import os
import sys
import time
import json
from dotenv import load_dotenv
load_dotenv()

# Make local imports work
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from params import ChatbotParams
from utils.rag.build_rag import chat_with_rag, chat_without_rag

def update_param(chatbot_model: str = None, with_rag: bool = None) -> None:
    """
    Update the chatbot parameters stored in params.json
    """

    # 讀取現有的 JSON
    with open("params.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)

    # 更新指定的 key
    if chatbot_model is not None:
        cfg["chatbot_model"] = chatbot_model
    if with_rag is not None:
        cfg["with_rag"] = with_rag

    # 寫回 JSON 檔
    with open("params.json", "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4, ensure_ascii=False)

    return

def ask_with_chatbot(query: str) -> str:
    with open("params.json", "r", encoding="utf-8") as f:
            cfg = json.load(f)

    params = ChatbotParams(
        emb_model=cfg["emb_model"],
        faiss_idx_path=cfg["faiss_idx_path"],
        k=cfg["k"],
        chatbot_model=cfg["chatbot_model"],
        judge_model=cfg["judge_model"],
        with_rag=cfg["with_rag"],
        openrouter_api_key=os.getenv("OPENROUTER_API_KEY")
    )

    if params.with_rag:
        rag_chain = chat_with_rag(params)
        reply = rag_chain.invoke(query)
        print(f"Reply: {reply}")
    else:
        worag_chain = chat_without_rag(params)
        reply = worag_chain.invoke(query)
        print(f"Reply: {reply}")

    return reply

def tackle_msg(msg: str) -> None:
    if msg == "/close_rag":
        try:
            print("1")
            update_param(with_rag=False)
            reply = "Success"
        except Exception as e:
            reply = "Failed"
            raise "Error"
    elif msg == "/open_rag":
        try:
            update_param(with_rag=True)
            reply = "Success"
        except Exception as e:
            reply = "Failed"
    else:
        reply = ask_with_chatbot(msg)
    return reply

if __name__ == "__main__":
    while True:
        i_path = "../../msg.txt"
        o_path = "../../msg2.txt"
        if os.path.exists(i_path):
            with open(i_path) as f:
                msg = f.read().strip()
            print(f"Received message: {msg}")
            if msg:
                reply = tackle_msg(msg)
                with open(o_path, "w") as f:
                    f.write(reply)
                os.remove(i_path)  # 清掉舊訊息
        time.sleep(1)