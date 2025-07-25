import os
import sys
import argparse
import json

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from utils.create_emb import get_embedding_model
from utils.process_faiss_idx import append_to_index

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

    embedding_model = get_embedding_model(args.model)
    file1 = "when are hops added to the brewing process?"
    append_to_index(args.faiss_idx_path, [file1], embedding_model)