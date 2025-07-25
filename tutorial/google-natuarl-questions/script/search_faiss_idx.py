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
    search_query(args.faiss_idx_path, embedding_model, query, k=5)