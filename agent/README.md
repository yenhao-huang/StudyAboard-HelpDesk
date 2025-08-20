# RAG Project

本專案包含 **RAG 架構**與 **模型設定**，提供完整的資料前處理、索引建立、檢索生成與結果評估流程。

---
## Project Structure

```
agent/
├── data/             # 原始資料與前處理後的資料存放區
├── exp/              # 實驗相關腳本與評估結果 (retrieval / generation / chunking)
├── index/            # 向量索引 (FAISS) 檔案
├── metadata/         # 資料與索引的中繼資訊 (uuid, chunk 設定等)
├── results/          # 最終輸出結果 (回答、模型比較等)
├── script/             # 執行流程與主要腳本
│   ├── data_preprocess/   # 資料前處理 (uuid 標註、chunk 切割)
│   ├── eval/              # 評估腳本 (retrieval / generation)
│   ├── visualization/     # 視覺化 (檢索與生成結果圖表化)
│   ├── build_faiss_idx.py # 建立 FAISS 索引
│   ├── chatbot_tgram.py   # Telegram Chatbot 主程式
│   ├── evaluate.py        # 評估入口 (retrieval/generation)
│   ├── params.json        # 預設參數 (JSON 格式)
│   ├── params.py          # 模型與檢索參數設定
│   ├── rag_main.py        # RAG 主程式 (核心執行入口)
│   └── update_config.py   # 更新與自訂 ChatbotParams
├── secrets/          # 憑證或金鑰設定 (避免上傳到公開 repo)
├── utils/              # 共用工具模組
│   ├── google_cloud_api/   # Google Cloud API 串接（檔案存取、雲端服務）
│   ├── model/              # 模型相關工具（載入、權重管理、推論支援）
│   └── rag/                # RAG 工具模組
│       ├── build_rag.py        # 構建 RAG pipeline
│       ├── common_utils.py     # RAG 共用函式（資料轉換、參數處理）
│       ├── create_emb.py       # 建立與管理 embedding 模型
│       ├── process_faiss_idx.py# FAISS 索引處理與更新
│       └── viz_rag.py          # 檢索與生成結果可視化
├── .env           # 環境變數
├── .gitignore     # 忽略檔案設定
└── README.md      # 專案說明文件
```


## How to Run

### 0. Data Preprocess

```bash
cd script/data_preprocess
python label_uuid.py  # 增加識別碼
```

### 1. 建立 FAISS Index

```bash
cd script
python build_faiss_idx.py
```

### 2. 執行 RAG

```bash
python rag_main.py
```

### 3. 評估

#### 評估 Chunking Strategy

```bash
cd ../exp
cd chunking_strategy
bash evaluate_retrie_{model_name}.sh
cd ..
```

#### 評估 Retrieved Model

```bash
bash evaluate_retrie_{model_name}.sh
```

#### 評估 Generation Model

```bash
bash evaluate_generation_{model_name}.sh
```

---

## 如何增加 LLM 支援模型

兩種設定方式：

1. 在 `rag_main/get_params` function 中挑選一個既有設定。
2. 使用自訂參數（custom setting）：
   在使用前執行以下指令，定義 `ChatbotParams`：

```bash
python update_config.py \
--emb_model ${EMB_MODEL} \
--faiss_idx_path ../index/${EMB_MODEL}_faiss_${CHUNK_SIZE} \
--k 5 \
--chatbot_model moonshotai/kimi-k2:free \
--judge_model google/gemma-3-27b-it:free
```

**參數說明：**

* `emb_model`：Embedding 模型名稱
* `faiss_idx_path`：FAISS 索引路徑
* `k`：檢索筆數
* `chatbot_model`：聊天模型
* `judge_model`：評估模型
* `with_rag`：是否啟用 RAG