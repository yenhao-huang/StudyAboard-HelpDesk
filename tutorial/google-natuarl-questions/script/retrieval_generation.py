import os
import sys
import argparse
import json

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

import torch
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from utils.process_faiss_idx import search_query
from openai import OpenAI

def create_parser():
    parser = argparse.ArgumentParser(description="Build FAISS index from JSON passages")
    
    parser.add_argument(
        "--model", 
        type=str, 
        default="sentence-transformers/all-MiniLM-L6-v2",
        help="HuggingFace embedding model name"
    )

    parser.add_argument(
        "--faiss_idx_path",
        type=str,
        default="index/nq_langchain_faiss",
        help="Input FAISS index"
    )
    return parser

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    embedding_model = HuggingFaceEmbeddings(
        model_name=args.model,
        model_kwargs={"device": device}
    )

    # User input
    query = input("Enter your query: ").strip()

    # Search
    results = search_query(args.faiss_idx_path, embedding_model, query, k=5)

    # Search
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        # Suggest: change to os.getenv() read api_key
        api_key="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",
    )

    context = "\n\n".join(
        [f"### paragraph_{i+1}\n{para}" for i, para in enumerate(results)]
    )

    # vuild prompt format
    prompt = f"""Context:
    {context}

    Question:
    {query}

    Answer:
    """

    completion = client.chat.completions.create(
        model="qwen/qwen3-coder:free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    print("Answer:\n", completion.choices[0].message.content)
