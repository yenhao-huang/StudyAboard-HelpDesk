import os
import sys
import argparse
from dotenv import load_dotenv

load_dotenv()

# Make local imports work
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.documents import Document
from langchain import hub
from IPython.display import display, Image

from utils.rag import create_emb  

def create_parser():
    p = argparse.ArgumentParser(description="Chatbot with/without RAG (LangChain)")
    p.add_argument("--emb_model", type=str,
                   default="Alibaba-NLP/gte-multilingual-base",
                   help="HuggingFace embedding model name")
    p.add_argument("--chatbot_model", type=str,
                   default="microsoft/mai-ds-r1:free",
                   help="Model name on OpenRouter")
    p.add_argument("--query", type=str,
                   default="請問役男的出入境須知",
                   help="User question")
    p.add_argument("--faiss_idx_path", type=str,
                   default="../index/alibaba_faiss",
                   help="Directory containing FAISS index")
    p.add_argument("--k", type=int, default=5, help="Top-k docs for retrieval")
    return p

def format_docs(docs: list[Document]) -> str:
    return "\n\n".join(d.page_content for d in docs)

def ask_with_rag(query: str) -> str:
    args = create_parser().parse_args([])  # 不從 CLI 讀參數
    args.query = query

    retriever = get_retriever(args.faiss_idx_path, args.embeddings, args.k)
    chat_with_rag(args.query, retriever, args.chatbot_model)

    return rag_chain.invoke(query)

def call_llm(chatbot_model):
    llm = ChatOpenAI(
        model=chatbot_model,
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0.2,
    )

    return llm

def get_retriever(faiss_idx_path, emb_model, k):
    # Get embedding model
    embeddings = create_emb.get_embedding_model(emb_model)

    # Load FAISS index and create retriever
    vectorstore = FAISS.load_local(
        faiss_idx_path,
        embeddings,
        allow_dangerous_deserialization=True,  # required for many FAISS saves
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    return retriever

def chat_without_rag(chatbot_model: str) -> object:
    llm = call_llm(chatbot_model)
    prompt_wo = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful, concise assistant."),
        ("human", "Question: {question}\n\nAnswer:")
    ])
    chain_wo = prompt_wo | llm | StrOutputParser()
    return chain_wo

def chat_with_rag(emb_model: str, faiss_idx_path: str, k: int, chatbot_model: str) -> object:
    retriever = get_retriever(faiss_idx_path, emb_model, k)
    
    prompt_rag = hub.pull("rlm/rag-prompt")
    llm = call_llm(chatbot_model)
    # RAG chain: map the user query to retriever -> format -> prompt -> llm
    chain_rag = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt_rag
        | llm
        | StrOutputParser()
    )

    return chain_rag


def save_chain_graph(
    chain: Runnable,
    file_path: str,
    method: str = "png"
) -> None:
    """
    將 LangChain Runnable graph 存成圖檔或文字檔。

    Args:
        chain (Runnable): 你的 Runnable chain
        file_path (str): 儲存檔案的路徑，例如 "rag_graph.png"
        method (str): "png", "ascii", or "mermaid"
    """
    try:
        graph = chain.get_graph()
        if method == "png":
            content = graph.draw_mermaid_png()
            with open(file_path, "wb") as f:
                f.write(content)
        elif method == "ascii":
            content = graph.draw_ascii()
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        elif method == "mermaid":
            content = graph.draw_mermaid()
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        else:
            print(f"[Error] Unsupported method: {method}")
        print(f"[Saved] Graph saved to {file_path}")
    except Exception as e:
        print(f"[Error] Failed to save graph: {e}")



def build_multiturn_rag_chain(emb_model: str, faiss_idx_path: str, k: int, chatbot_model: str):
    retriever = get_retriever(faiss_idx_path, embeddings, k)
    llm = call_llm(chatbot_model)
    
    # 1) 問題改寫（含歷史）：(chat_history, question) -> standalone query
    prompt_w_hist = ChatPromptTemplate.from_messages([
        ("system",
        "You reformulate the user's latest question into a standalone search query, "
        "grounded by the chat history. Do NOT answer."),
        MessagesPlaceholder("chat_history"),
        ("human", "{question}")
    ])

    question_condenser = prompt_w_hist | llm | StrOutputParser()

    # 2) 用改寫後的查詢去檢索
    def retrieve_with_history(inputs):
        # inputs 會帶有 {"question": str, "chat_history": [...]}
        standalone = question_condenser.invoke(inputs)
        docs = retriever.invoke(standalone)
        return format_docs(docs)

    # 3) RAG 主鏈：取 context + question → 回答（含歷史）
    ANSWER_PROMPT = ChatPromptTemplate.from_messages([
        ("system",
        "You are a helpful, concise assistant. Use the provided context to answer. "
        "If the answer isn't contained in the context, say you're unsure."),
        MessagesPlaceholder("chat_history"),
        ("human", "Context:\n{context}\n\nQuestion: {question}\n\nAnswer:")
    ])

    rag_core = (
        RunnableMap({
            "context": retrieve_with_history,
            "question": RunnablePassthrough(),
        })
        | ANSWER_PROMPT
        | llm
        | StrOutputParser()
    )

    # 4) 多輪歷史封裝（用 session_id 管理）
    store = {}  # {session_id: ChatMessageHistory}

    def get_session_history(session_id: str):
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]

    rag_with_history = RunnableWithMessageHistory(
        rag_core,
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history",
        output_messages_key="output"
    )
    return rag_with_history

def test():
    args = create_parser().parse_args()
    print("Questions:", args.query)

    # ===== A) Chat WITHOUT RAG =====
    chain_wo = chat_without_rag(args.chatbot_model)
    save_chain_graph(chain_wo, "../metadata/worag_graph.png", method="png")
    chain_rag = chat_with_rag(args.emb_model, args.faiss_idx_path, args.k, args.chatbot_model)
    save_chain_graph(chain_rag, "../metadata/rag_graph.png", method="png")
    print("=== Answer without RAG ===")
    print(chain_wo.invoke({"question": args.query}))
    print()

    print("=== Answer with RAG ===")
    print(chain_rag.invoke(args.query))
 
if __name__ == "__main__":
    #test()
    evaluate()
