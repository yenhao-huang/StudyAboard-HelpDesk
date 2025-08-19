import os
import sys
import argparse
from dotenv import load_dotenv

load_dotenv()

# Make local imports work
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

import json

from utils.rag import create_emb
from utils.rag.build_rag import chat_without_rag, chat_with_rag
from utils.rag.viz_rag import save_chain_graph
import params as PARAMS

def create_parser():
    p = argparse.ArgumentParser(description="Chatbot with/without RAG (LangChain)")
    p.add_argument("--query", type=str,
                   default="請問役男的出入境須知",
                   help="User question")
    p.add_argument("--openrouter_setting", type=int,
                   default=0,
                   help="OpenRouter API key")
    p.add_argument("--setting", type=str,
                   default="alibaba",
                   choices=["alibaba", "sentencetf", "alibaba_worag"],
                   help="RAG setting to use")
    return p


def get_params(setting: str):
    """
    根據設定名稱返回對應的參數。
    """
    params = None
    if setting == "alibaba":
        params = PARAMS.PARAMS_ALIBABA
    elif setting == "sentencetf":
        params = PARAMS.PARAMS_SENTENCE
    elif setting == "alibaba_worag":
        params = PARAMS.PARAMS_ALIBABA_WORAG
    elif setting == "mistral_worag":
        params = PARAMS.PARAMS_MISTRAL_WORAG
    elif setting == "mistral":
        params = PARAMS.PARAMS_MISTRAL
    elif setting == "deepseek_worag":
        params = PARAMS.PARAMS_DEEPSEEK_WORAG
    elif setting == "deepseek":
        params = PARAMS.PARAMS_DEEPSEEK
    elif setting == "qwen3":
        params = PARAMS.PARAMS_EMB_QWEN3
    elif setting == "qwen3_small":
        params = PARAMS.PARAMS_EMB_QWEN3_SMALL
    elif setting == "baai":
        params = PARAMS.PARAMS_EMB_BAAI
    elif setting == "baai_bge_m3":
        params = PARAMS.PARAMS_EMB_BAAI_BGE_M3
    elif setting == "tencent_conan":
        params = PARAMS.PARAMS_EMB_TENCENT_CONAN
    elif setting == "custom":
        with open("params.json", "r", encoding="utf-8") as f:
                cfg = json.load(f)

        params = PARAMS.ChatbotParams(
            emb_model=cfg["emb_model"],
            faiss_idx_path=cfg["faiss_idx_path"],
            k=cfg["k"],
            chatbot_model=cfg["chatbot_model"],
            judge_model=cfg["judge_model"],
            with_rag=cfg["with_rag"],
        )
    else:
        raise ValueError(f"Unsupported setting: {setting}")

    # 設定 OpenRouter API key
    if params.openrouter_api_key_id == 0:
        params.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    elif params.openrouter_api_key_id == 1:
        params.openrouter_api_key = os.getenv("OPENROUTER_API_KEY2")
    else:
        raise ValueError(f"Unsupported OpenRouter setting: {params.openrouter_setting}")

    return params


def test():
    args = create_parser().parse_args()
    params = get_params(args.setting)
    print("Questions:", args.query)

    # ===== A) Chat WITHOUT RAG =====
    chain_wo = chat_without_rag(params)
    save_chain_graph(chain_wo, "../metadata/worag_graph.png", method="png")
    chain_rag = chat_with_rag(params)
    save_chain_graph(chain_rag, "../metadata/rag_graph.png", method="png")
    print("=== Answer without RAG ===")
    print(chain_wo.invoke({"question": args.query}))
    print()

    print("=== Answer with RAG ===")
    print(chain_rag.invoke(args.query))
 
if __name__ == "__main__":
    # TODO: ask_with_rag
    test()
