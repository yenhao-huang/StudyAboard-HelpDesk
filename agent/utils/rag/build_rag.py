from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.documents import Document
from langchain import hub
from IPython.display import display, Image

from . import create_emb

def format_docs(docs: list[Document]) -> str:
    return "\n\n".join(d.page_content for d in docs)

def chat_without_rag(params: object) -> object:
    llm = call_llm(params.chatbot_model, params.openrouter_api_key)
    prompt_wo = ChatPromptTemplate.from_messages([
        ("system", 
        "你是一個有幫助且簡潔的助理。"
        ),
        
        ("human", 
        "問題：{question}\n\n"
        "回答:\n"
        "⚠️ 請務必遵循以下規則：\n"
        "1. 輸出不要使用任何 Markdown 標記（例如 ** 或 ##），只輸出純文字。"
        "2. 輸出不要使用任何 Markdown 標記（例如 ** 或 ##），只輸出純文字。"
        "3. 輸出不要使用任何 Markdown 標記（例如 ** 或 ##），只輸出純文字。"
        "4. 輸出不要使用任何 Markdown 標記（例如 ** 或 ##），只輸出純文字。"
        "5. 輸出不要使用任何 Markdown 標記（例如 ** 或 ##），只輸出純文字。"
        )
    ])
    chain_wo = prompt_wo | llm | StrOutputParser()
    return chain_wo

def chat_with_rag(params: object) -> object:
    retriever = get_retriever(params.faiss_idx_path, params.emb_model, params.k)
    prompt_rag = ChatPromptTemplate.from_messages([
        ("system", 
        "你是一個有幫助且簡潔的助理。"
        ),
        
        ("human", 
        "檢索內容：\n{context}\n\n"
        "問題：{question}\n\n"
        "⚠️ 請務必遵循以下規則：\n"
        "1. 只根據提供的檢索內容回答問題。\n"
        "2. 如果檢索內容中沒有答案，請回答『根據提供的內容無法回答』。\n"
        "3. 請用中文作答，不得使用其他語言。\n"
        "4. 不要使用任何 Markdown 標記（例如 ** 或 ##），只輸出純文字。"
        )
    ])
    llm = call_llm(params.chatbot_model, params.openrouter_api_key)
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

def chat_with_rag_style(params: object) -> object:
    retriever = get_retriever(params.faiss_idx_path, params.emb_model, params.k)
    
    prompt_rag = ChatPromptTemplate.from_messages([
        ("system", 
        "你是一個有幫助且簡潔的助理。"
        ),
        
        ("human", 
        "檢索內容：\n{context}\n\n"
        "問題：{question}\n\n"
        "⚠️ 請務必遵循以下規則：\n"
        "1. 根據提供的檢索內容回答問題。\n"
        "2. 請用中文作答，不得使用其他語言。\n"
        "3. 回答時要重點清晰、不要冗長。\n"
        "4. 回答要更加自然、友善，就像和朋友聊天一樣，請模仿下方 <few_shot_examples> 的風格。\n"
        "5. 不要使用任何 Markdown 標記（例如 ** 或 ##），只輸出純文字。\n\n"
        
        "<few_shot_examples>\n"
        "  <example>\n"
        "    <question>我還沒當兵，但被推薦去德國研究，請問最長可以待多久？</question>\n"
        "    <answer>如果你是還在念書的役男，那最長可以待一年；但如果不是在學身份，就只能最多六個月。希望這樣能幫到你！</answer>\n"
        "  </example>\n\n"
        "  <example>\n"
        "    <question>請問替代役可以申請延期嗎？</question>\n"
        "    <answer>可以的，但需要符合特定條件，比如繼續升學或特殊家庭狀況。建議你確認一下相關規定，再遞交申請。希望有幫助！</answer>\n"
        "  </example>\n"
        "</few_shot_examples>\n\n"
        )
    ])
    llm = call_llm(params.chatbot_model, params.openrouter_api_key)
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

def call_llm(chatbot_model: object, api_key: str):
    
    llm = ChatOpenAI(
        model=chatbot_model,
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        temperature=0.1,
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
