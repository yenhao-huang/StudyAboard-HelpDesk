import argparse
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from langchain_community.retrievers import BM25Retriever

from utils.rag import create_emb, process_faiss_idx, common_utils

def create_parser():
    parser = argparse.ArgumentParser(description="Build FAISS index from JSON passages")

    parser.add_argument(
        "--doc_path",
        type=str,
        default="data/docs",
        help="Path to retrival file containing raw text passages"
    )
    return parser

if __name__ == "__main__":

    parser = create_parser()
    args = parser.parse_args()

    # get files in data directory
    data_dir = os.path.join(project_root, args.doc_path)
    files = common_utils.list_all_files(data_dir)
    print(files)

    # 建立 BM25Retriever, input list[str]
    #retriever = BM25Retriever.from_texts(docs)