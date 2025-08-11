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

        required_cols = ["question", "answer", "source", "class", "uuid"]
        page_conent_col = "answer"
        metadata_cols = ["question", "class", "source", "uuid"]

        # Ensure all required columns are present
        missing = set(required_cols) - set(df.columns)
        if missing:
            raise KeyError(f"{p} missing columns: {sorted(missing)}")

        # Clean missing values and convert all to string
        df = df[required_cols].fillna("").astype(str)

        # Convert each row into a Document
        for row in df[required_cols].itertuples(index=False, name=None):
            metadata = {}
            for col_name, item in zip(required_cols, row):
                if col_name in metadata_cols:
                    metadata[col_name] = item
                elif col_name == page_conent_col:
                    a = item

            docs.append(
                Document(
                    page_content=a,
                    metadata=metadata
                )
            )

    return docs

def add_chunk_id(docs: List[Document]) -> List[Document]:
    for idx, doc in enumerate(docs):
        if "uuid" not in doc.metadata:
            raise KeyError("Each original Document must have a 'uuid' in metadata before splitting.")
        chunk_id = f"{doc.metadata['uuid']}_{idx}"
        doc.metadata["chunk_id"] = chunk_id

def save_chunk2id(docs: List[Document], output_path: str):
    chunks = []
    chunk_ids = []
    class_all = []
    answers = []

    for doc in docs:
        question = doc.metadata.get("question", "")
        answer = doc.page_content
        chunk_id = doc.metadata.get("chunk_id", "")
        c = doc.metadata.get("class", "")
        if question and chunk_id and c and answer:
            chunks.append(question)
            chunk_ids.append(chunk_id)
            class_all.append(c)
            answers.append(answer)

    # Create DataFrame for chunk_id mapping
    df_chunk2id = pd.DataFrame({
        "class": class_all,
        "chunk": chunks,
        "answer": answers,
        "chunk_id": chunk_ids,
    })

    df_chunk2id.to_csv(output_path, index=False, encoding="utf-8")

def split(docs: List[Document], chunk_size: int = 512) -> List[Document]:
    """
    Split Documents into smaller chunks of specified size.
    """
    if not docs:
        raise ValueError("No documents provided; cannot split empty list.")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=200)
    all_splits = text_splitter.split_documents(docs)
    add_chunk_id(all_splits)
    save_chunk2id(all_splits, "../data/metadata/chunk2id.csv")
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

