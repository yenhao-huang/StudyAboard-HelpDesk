# app/services/model.py
import os
from dotenv import load_dotenv
load_dotenv()

from agent.utils.rag.build_rag import chat_with_rag
from agent.script.params import ChatbotParams

def ask_with_rag(query: str) -> str:
    params = ChatbotParams(
        emb_model="Alibaba-NLP/gte-multilingual-base",
        faiss_idx_path="agent/index/alibaba_faiss",
        k=5,
        chatbot_model="moonshotai/kimi-k2:free",
        judge_model="google/gemma-3-27b-it:free",
        with_rag=False,
        openrouter_api_key=os.getenv("OPENROUTER_API_KEY")
    )

    rag_chain = chat_with_rag(params)
    return rag_chain.invoke(query)


def ask_model(message: str) -> str:
    try:
        return ask_with_rag(message)
    except Exception as e:
        return f"Error: {e}"
