import os
import json
import torch
from pathlib import Path
from typing import Iterable, List
import pandas as pd
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings  # interface
from langchain_text_splitters import RecursiveCharacterTextSplitter

REQUIRED_COLS = ["question", "answer", "source", "class"]

def load_doc(files: Iterable[str]) -> List[Document]:
    """
    Load Q/A rows from CSV files and convert them to LangChain Documents.
    Each row -> page_content: "Question: ...\nAnswer: ...", metadata: {"class": ..., "source": ...}
    """
    docs: List[Document] = []
    for path in files:
        p = Path(path)
        if p.suffix.lower() != ".csv":
            raise ValueError(f"Unsupported file format: {p}. Only .csv is supported.")

        # Read CSV
        df = pd.read_csv(p, encoding="utf-8")

        # Ensure all required columns are present
        missing = set(REQUIRED_COLS) - set(df.columns)
        if missing:
            raise KeyError(f"{p} missing columns: {sorted(missing)}")

        # Clean missing values and convert all to string
        df = df[REQUIRED_COLS].fillna("").astype(str)

        # Convert each row into a Document
        for row in df[REQUIRED_COLS].itertuples(index=False, name=None):
            q, a, s, c = row

            docs.append(
                Document(
                    page_content=a,
                    metadata={"question": q, "class": c, "source": s}
                )
            )
    return docs

def split(docs: List[Document], chunk_size: int = 512) -> List[Document]:
    """
    Split Documents into smaller chunks of specified size.
    """
    if not docs:
        raise ValueError("No documents provided; cannot split empty list.")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=200)
    all_splits = text_splitter.split_documents(docs)
    return all_splits

def build_new_index(docs: List[Document], index_dir: str, embedding_model: Embeddings) -> FAISS:
    """
    Build a FAISS index from Documents and save it into a directory.

    Args:
        docs: List of LangChain Documents to index.
        index_dir: Directory path where the FAISS index will be saved.
        embedding_model: Embedding model implementing the `Embeddings` interface.

    Returns:
        FAISS vectorstore object
    """
    if not docs:
        raise ValueError("No documents provided; abort building index.")

    index_path = Path(index_dir)
    index_path.mkdir(parents=True, exist_ok=True)

    # Create FAISS index from documents
    vectorstore = FAISS.from_documents(docs, embedding_model)

    # Save the index to disk (writes multiple files under index_dir)
    vectorstore.save_local(str(index_path))
    print(f"[✓] New index built and saved to {index_path.resolve()}")
    return vectorstore

