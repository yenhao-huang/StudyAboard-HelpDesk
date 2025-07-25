import os
import sys
import argparse
import json

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from utils.create_emb import get_embedding_model
from utils.process_faiss_idx import build_new_index

def create_parser():
    parser = argparse.ArgumentParser(description="Build FAISS index from JSON passages")
    
    parser.add_argument(
        "--model", 
        type=str, 
        default="sentence-transformers/all-MiniLM-L6-v2",
        help="HuggingFace embedding model name"
    )

    parser.add_argument(
        "--doc_path",
        type=str,
        default="data/nq_passages.json",
        help="Path to JSON file containing raw text passages"
    )

    parser.add_argument(
        "--faiss_idx_path",
        type=str,
        default="index/nq_langchain_faiss",
        help="Output path to save FAISS index"
    )
    return parser

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    embedding_model = get_embedding_model(args.model)
    build_new_index(args.doc_path, args.faiss_idx_path, embedding_model)