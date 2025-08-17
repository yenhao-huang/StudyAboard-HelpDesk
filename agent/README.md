* RAG
* Model

## How to Run
0. data preprocess

cd script/data_preprocess
python label_uuid.py # 增加識別碼

1. 建立 faiss index
cd script
python build_faiss_idx.py

2. 執行 RAG
python rag_main.py

3. 評估 retrieved data

cd ../exp
bash evaluate_generation.sh
bash evaluate_retrie_alibaba.sh

### Chatbot 參數設定
定義 `ChatbotParams`，集中管理模型與檢索設定：

- `emb_model`：Embedding 模型名稱  
- `faiss_idx_path`：FAISS 索引路徑  
- `k`：檢索筆數  
- `chatbot_model`：聊天模型  
- `judge_model`：評估模型  
- `with_rag`：是否啟用 RAG  

內建三組參數：
1. **`PARAMS_ALIBABA_WORAG`** — Alibaba Embedding，關閉 RAG（純生成）  
2. **`PARAMS_ALIBABA`** — Alibaba Embedding，啟用 RAG  
3. **`PARAMS_SENTENCE`** — Sentence-Transformers Embedding（英文優化），啟用 RAG

### Challenges: 搜尋出來的結果很差?
原因
* 索引裡根本沒這筆
* 嵌入模型不對齊 (中/英文)

## 增加 LLM 支援模型

1. scripts/params.py 加入

PARAMS_MISTRAL = ChatbotParams(
    emb_model="Alibaba-NLP/gte-multilingual-base",
    faiss_idx_path="../index/alibaba_faiss",
    k=5,
    chatbot_model="mistralai/mistral-nemo:free",
    judge_model="google/gemma-3-27b-it:free",
)

2. scripts/rag_main.py get_main() 增加判斷