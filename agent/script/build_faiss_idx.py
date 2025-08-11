import os
import sys
import argparse
import json
import gdown
import tempfile

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from utils.rag import create_emb, process_faiss_idx
from utils.google_cloud_api.google_drive_api import get_files_in_folder

def create_parser():
    parser = argparse.ArgumentParser(description="Build FAISS index from JSON passages")
    
    parser.add_argument(
        "--model", 
        type=str, 
        default="Alibaba-NLP/gte-multilingual-base",
        help="HuggingFace embedding model name"
    )

    parser.add_argument(
        "--doc_path",
        type=str,
        default="data/docs/common_questions",
        help="Path to retrival file containing raw text passages"
    )

    parser.add_argument(
        "--chunk_size",
        type=int,
        default=512,
        help="Size of text chunks to split documents into"
    )

    parser.add_argument(
        "--faiss_idx_path",
        type=str,
        default="../index/alibaba_faiss",
        help="Output path to save FAISS index"
    )
    return parser

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    # get files in data directory
    data_dir = os.path.join(project_root, args.doc_path)
    files = []
    for f in os.listdir(data_dir):
        path = os.path.join(data_dir, f)
        if os.path.isfile(path):
            files.append(path)

    # load documents from files
    docs = process_faiss_idx.load_doc(files)
    all_split = process_faiss_idx.split(docs, chunk_size=args.chunk_size)

    # build FAISS index
    embedding_model = create_emb.get_embedding_model(args.model)
    process_faiss_idx.build_new_index(all_split, args.faiss_idx_path, embedding_model)