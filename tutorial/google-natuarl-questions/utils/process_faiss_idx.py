import os

from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
import json
import torch

def build_new_index(json_path: str, index_path: str, embedding_model):
    with open(json_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    queries = raw_data["query"]
    answers = raw_data["answer"]

    # 確保 query 和 answer 數量對齊
    assert len(queries) == len(answers)

    docs = [
        Document(page_content=f"Question: {q}\nAnswer: {a}")
        for q, a in zip(queries, answers)
    ]

    vectorstore = FAISS.from_documents(docs, embedding_model)

    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    vectorstore.save_local(index_path)
    print(f"[✓] New index built and saved to {index_path}")


def append_to_index(index_path: str, new_texts: list, embedding_model):
    new_docs = [Document(page_content=txt) for txt in new_texts]

    vectorstore = FAISS.load_local(index_path, embeddings=embedding_model, allow_dangerous_deserialization=True)
    vectorstore.add_documents(new_docs)
    vectorstore.save_local(index_path)
    print(f"[+] Added {len(new_docs)} docs to existing index: {index_path}")

def search_query(index_path: str, embedding_model, query: str, k: int = 5):
    vectorstore = FAISS.load_local(index_path, embeddings=embedding_model, allow_dangerous_deserialization=True)

    results = vectorstore.similarity_search(query, k=k)

    print(f"\n🔍 Top-{k} results for query: \"{query}\"\n")
    for i, doc in enumerate(results):
        print(f"[{i+1}] {doc.page_content}\n{'-'*50}")
    
    return results

