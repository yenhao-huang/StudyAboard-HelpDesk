# app/services/model.py
from agent.script.rag_main import ask_with_rag

def ask_model(message: str) -> str:
    try:
        return ask_with_rag(message)
    except Exception as e:
        return f"Error: {e}"
