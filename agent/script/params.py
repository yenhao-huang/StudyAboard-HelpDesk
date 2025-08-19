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

PARAMS_EMB_TENCENT_CONAN = ChatbotParams(
    emb_model="TencentBAC/Conan-embedding-v1",
    faiss_idx_path="../index/tencent_conan_faiss",
    k=5,
    chatbot_model="moonshotai/kimi-k2:free",
    judge_model="google/gemma-3-27b-it:free",
)

PARAMS_EMB_BAAI_BGE_M3 = ChatbotParams(
    emb_model="BAAI/bge-m3",
    faiss_idx_path="../index/baai_bge_m3_faiss",
    k=5,
    chatbot_model="moonshotai/kimi-k2:free",
    judge_model="google/gemma-3-27b-it:free",
)

PARAMS_EMB_BAAI = ChatbotParams(
    emb_model="BAAI/bge-large-zh-v1.5",
    faiss_idx_path="../index/baai_faiss",
    k=5,
    chatbot_model="moonshotai/kimi-k2:free",
    judge_model="google/gemma-3-27b-it:free",
)

PARAMS_EMB_QWEN3 = ChatbotParams(
    emb_model="Qwen/Qwen3-Embedding-8B",
    faiss_idx_path="../index/qwen3_faiss",
    k=5,
    chatbot_model="moonshotai/kimi-k2:free",
    judge_model="google/gemma-3-27b-it:free",
)

PARAMS_EMB_QWEN3_SMALL = ChatbotParams(
    emb_model="Qwen/Qwen3-Embedding-0.6B",
    faiss_idx_path="../index/qwen3_faiss_small",
    k=5,
    chatbot_model="moonshotai/kimi-k2:free",
    judge_model="google/gemma-3-27b-it:free",
)

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
