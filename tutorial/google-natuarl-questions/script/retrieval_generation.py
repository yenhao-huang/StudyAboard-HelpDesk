import os
import sys

# Add the project root to sys.path so local imports work
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

import argparse
from dotenv import load_dotenv
load_dotenv()
import json
import torch
from openai import OpenAI
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from utils.process_faiss_idx import search_query

def create_parser():
    parser = argparse.ArgumentParser(description="Chatbot with or without RAG using FAISS and LLM")
    
    parser.add_argument(
        "--emb_model", 
        type=str, 
        default="sentence-transformers/all-MiniLM-L6-v2",
        help="HuggingFace embedding model name"
    )

    parser.add_argument(
        "--chatbot_model", 
        type=str, 
        default="deepseek/deepseek-r1-0528-qwen3-8b:free",
        help="Chatbot model from OpenRouter"
    )

    parser.add_argument(
        "--query", 
        type=str, 
        default="Who produces the most wool in the world?",
        help="User's query"
    )

    parser.add_argument(
        "--faiss_idx_path",
        type=str,
        default="index/nq_langchain_faiss",
        help="Path to FAISS index directory"
    )
    return parser

def chat_with_llm(client, model_name, prompt):
    # Send prompt to LLM via OpenRouter API
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )
    return response

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    # Initialize embedding model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    embedding_model = HuggingFaceEmbeddings(
        model_name=args.emb_model,
        model_kwargs={"device": device}
    )

    # Initialize OpenRouter client
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")  # Recommended to store key in environment
    )

    # Get user input query
    query = args.query.strip()

    # === Chat without RAG ===
    prompt_wo_rag = f"""
    Question: {query}

    Answer:
    """
    response = chat_with_llm(client, args.chatbot_model, prompt_wo_rag)
    print("Answer without RAG:\n", response.choices[0].message.content)

    # === Chat with RAG (retrieve related context first) ===
    results = search_query(args.faiss_idx_path, embedding_model, query, k=5)

    # Format retrieved paragraphs
    context = "\n\n".join(
        [f"### paragraph_{i+1}\n{para}" for i, para in enumerate(results)]
    )

    # Build full prompt with context
    prompt_with_rag = f"""Context:
    {context}

    Question:
    {query}

    Answer:
    """

    response = chat_with_llm(client, args.chatbot_model, prompt_with_rag)
    print("Answer with RAG:\n", response.choices[0].message.content)
