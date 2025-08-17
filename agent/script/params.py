from dataclasses import dataclass

@dataclass
class ChatbotParams:
    emb_model: str
    faiss_idx_path: str
    k: int
    chatbot_model: str
    judge_model: str
    with_rag: bool = True
    openrouter_api_key_id: int = 0
    openrouter_api_key: str = None

PARAMS_ALIBABA_WORAG = ChatbotParams(
    emb_model="Alibaba-NLP/gte-multilingual-base",
    faiss_idx_path="../index/alibaba_faiss",
    k=5,
    chatbot_model="moonshotai/kimi-k2:free",
    judge_model="google/gemma-3-27b-it:free",
    with_rag=False,
)

PARAMS_ALIBABA = ChatbotParams(
    emb_model="Alibaba-NLP/gte-multilingual-base",
    faiss_idx_path="../index/alibaba_faiss",
    k=5,
    chatbot_model="moonshotai/kimi-k2:free",
    judge_model="google/gemma-3-27b-it:free",
)

PARAMS_MISTRAL_WORAG = ChatbotParams(
    emb_model="Alibaba-NLP/gte-multilingual-base",
    faiss_idx_path="../index/alibaba_faiss",
    k=5,
    chatbot_model="mistralai/mistral-nemo:free",
    judge_model="google/gemma-3-27b-it:free",
    with_rag=False,
)

PARAMS_MISTRAL = ChatbotParams(
    emb_model="Alibaba-NLP/gte-multilingual-base",
    faiss_idx_path="../index/alibaba_faiss",
    k=5,
    chatbot_model="mistralai/mistral-nemo:free",
    judge_model="google/gemma-3-27b-it:free",
)

PARAMS_DEEPSEEK_WORAG = ChatbotParams(
    emb_model="Alibaba-NLP/gte-multilingual-base",
    faiss_idx_path="../index/alibaba_faiss",
    k=5,
    chatbot_model="deepseek/deepseek-r1:free",
    judge_model="google/gemma-3-27b-it:free",
)

PARAMS_DEEPSEEK = ChatbotParams(
    emb_model="Alibaba-NLP/gte-multilingual-base",
    faiss_idx_path="../index/alibaba_faiss",
    k=5,
    chatbot_model="deepseek/deepseek-r1:free",
    judge_model="google/gemma-3-27b-it:free",
)


PARAMS_SENTENCE = ChatbotParams(
    emb_model="sentence-transformers/all-MiniLM-L6-v2",
    faiss_idx_path="../index/sentencetransformer_faiss",
    k=5,
    chatbot_model="moonshotai/kimi-k2:free",
    judge_model="google/gemma-3-27b-it:free",
)
