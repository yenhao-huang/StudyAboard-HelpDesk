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

def load_csvfile(path: Path):
    # Read CSV
    df = pd.read_csv(path, encoding="utf-8")

    required_cols = ["question", "answer", "source", "class", "uuid"]
    page_content_col = "answer"
    metadata_cols = ["question", "class", "source", "uuid"]

    # Ensure all required columns are present
    missing = set(required_cols) - set(df.columns)
    if missing:
        raise KeyError(f"{path} missing columns: {sorted(missing)}")

    # Clean missing values and convert all to string
    df = df[required_cols].fillna("").astype(str)

    # Convert each row into a Document
    docs = []
    for row in df[required_cols].itertuples(index=False, name=None):
        metadata = {}
        for col_name, item in zip(required_cols, row):
            if col_name in metadata_cols:
                metadata[col_name] = item
            elif col_name == page_content_col:
                a = item

        page_content = f"Q:{metadata['question']}\nA:{a}"
        docs.append(
            Document(
                page_content=page_content,
                metadata=metadata
            )
        )

    return docs

def load_jsonfile(path: Path):
    '''
    4 field: id, url, content, created_at
    '''
    # Read JSON file
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if len(data) != 1:
        raise ValueError(f"Expected exactly one JSON object in {path}, found {len(data)}")
    
    d = data[0] 
    doc = Document(
        page_content=d["content"],
        metadata={
            "uuid": d["id"],
            "url": d["url"],
            "created_at": d["created_at"]
        }
    )

    return doc

def load_doc(files: Iterable[str]) -> List[Document]:
    """
    Load Q/A rows from CSV files and convert them to LangChain Documents.
    Each row -> page_content: "Question: ...\nAnswer: ...", metadata: {"class": ..., "source": ...}
    """
    docs_all: List[Document] = []
    for path in files:
        p = Path(path)
        if p.suffix.lower() == ".csv":
            docs = load_csvfile(p)
            for doc in docs:
                docs_all.append(doc)
        elif p.suffix.lower() == ".json":
            doc = load_jsonfile(p)
            docs_all.append(doc)
        else:
            raise ValueError(f"Unsupported file format: {p}. Only .csv and .json are supported.")

    return docs_all

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

