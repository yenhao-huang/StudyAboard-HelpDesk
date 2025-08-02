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
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain import hub

from utils.rag import create_emb  

def create_parser():
    p = argparse.ArgumentParser(description="Chatbot with/without RAG (LangChain)")
    p.add_argument("--emb_model", type=str,
                   default="Alibaba-NLP/gte-multilingual-base",
                   help="HuggingFace embedding model name")
    p.add_argument("--chatbot_model", type=str,
                   default="deepseek/deepseek-r1-0528-qwen3-8b:free",
                   help="Model name on OpenRouter")
    p.add_argument("--query", type=str,
                   default="為什麼可以免費代辦?",
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

    embeddings = create_emb.get_embedding_model(args.emb_model)
    vectorstore = FAISS.load_local(
        "agent/index/alibaba_faiss", embeddings, allow_dangerous_deserialization=True
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": args.k})

    llm = ChatOpenAI(
        model=args.chatbot_model,
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0.2,
    )

    prompt_rag = hub.pull("rlm/rag-prompt")
    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt_rag
        | llm
        | StrOutputParser()
    )

    return rag_chain.invoke(query)

def main():
    args = create_parser().parse_args()
    print("Questions:", args.query)
    # --- Embeddings ---
    embeddings = create_emb.get_embedding_model(args.emb_model)

    # --- LLM (OpenRouter via LangChain) ---
    llm = ChatOpenAI(
        model=args.chatbot_model,
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0.2,
    )

    # ===== A) Chat WITHOUT RAG =====
    prompt_wo = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful, concise assistant."),
        ("human", "Question: {question}\n\nAnswer:")
    ])
    chain_wo = prompt_wo | llm | StrOutputParser()
    print("=== Answer without RAG ===")
    print(chain_wo.invoke({"question": args.query}))
    print()

    # ===== B) Chat WITH RAG =====
    # Load FAISS index and create retriever
    vectorstore = FAISS.load_local(
        args.faiss_idx_path,
        embeddings,
        allow_dangerous_deserialization=True,  # required for many FAISS saves
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": args.k})
    def check_retrived_data():
        docs = vectorstore.similarity_search_with_score(args.query, k=args.k)
        for d, s in docs:
            print(f"score={s:.4f}  {d}")
    # check_retrived_data()
    prompt_rag = hub.pull("rlm/rag-prompt")

    # RAG chain: map the user query to retriever -> format -> prompt -> llm
    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt_rag
        | llm
        | StrOutputParser()
    )

    print("=== Answer with RAG ===")
    print(rag_chain.invoke(args.query))

if __name__ == "__main__":
    main()
