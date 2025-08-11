from dataclasses import dataclass

@dataclass
class ChatbotParams:
    emb_model: str = "Alibaba-NLP/gte-multilingual-base"
    faiss_idx_path: str = "../index/alibaba_faiss"
    k: int = 5
    chatbot_model: str = "moonshotai/kimi-k2:free"
'''
# outdated, not used idx
class ChatbotParams:
    emb_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    faiss_idx_path: str = "../index/sentencetransformer_faiss"
    k: int = 5
    chatbot_model: str = "moonshotai/kimi-k2:free"
'''
PARAMS = ChatbotParams()