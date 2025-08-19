import argparse
import json

def update_param(
    emb_model: str = None,
    faiss_idx_path: str = None,
    k: str = None,
    chatbot_model: str = None,
    judge_model: str = None,
    with_rag: bool = None
) -> None:
    """
    Update the chatbot parameters stored in params.json
    """
    # 讀取現有的 JSON
    with open("params.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)

    # 更新指定的 key
    if emb_model is not None:
        cfg["emb_model"] = emb_model
    if faiss_idx_path is not None:
        cfg["faiss_idx_path"] = faiss_idx_path
    if k is not None:
        cfg["k"] = k
    if chatbot_model is not None:
        cfg["chatbot_model"] = chatbot_model
    if judge_model is not None:
        cfg["judge_model"] = judge_model
    if with_rag is not None:
        cfg["with_rag"] = with_rag

    # 寫回 JSON 檔
    with open("params.json", "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4, ensure_ascii=False)

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update chatbot params.json")

    parser.add_argument("--emb_model", type=str, help="Embedding model name")
    parser.add_argument("--faiss_idx_path", type=str, help="Path to FAISS index")
    parser.add_argument("--k", type=int, help="Number of nearest neighbors")
    parser.add_argument("--chatbot_model", type=str, help="Chatbot model name")
    parser.add_argument("--judge_model", type=str, help="Judge model name")
    parser.add_argument(
        "--with_rag", 
        type=lambda x: x.lower() in ["true", "1", "yes"], 
        help="Enable retrieval-augmented generation (True/False)"
    )

    args = parser.parse_args()

    update_param(
        emb_model=args.emb_model,
        faiss_idx_path=args.faiss_idx_path,
        k=args.k,
        chatbot_model=args.chatbot_model,
        judge_model=args.judge_model,
        with_rag=args.with_rag
    )
