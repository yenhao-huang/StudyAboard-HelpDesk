# 留學代辦客服

基於 RAG 的**留學代辦客服系統**，整合LLM API、後端服務與 Telegram 前端，協助用戶快速獲取正確資訊，降低地域性問題造成的幻覺。

**Results**

* **Retrieval Precision\@5**：85.5%
* **Generation Demo**：

<video src="metadata/rag_chabot.mp4" controls width="600"></video>

---

## **Project Structure**

```
RAG-CHATBOT/
├── agent/                 # LLM + RAG API
├── tutorial/              # RAG 練習與範例
├── telegram_frontend.py   # Telegram Bot 前端
├── .env                   # 環境變數 (需自行建立)
├── .gitignore
└── README.md
```

---

## **Installation**

```bash
git clone git@github.com:yenhao-huang/RAG-chatbot.git
cd RAG-chatbot
pip install -r requirements.txt
```

建立 `.env` 檔案：

```bash
cp .env.example .env
```

在 `.env` 中設定：

```dotenv
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENROUTER_API_KEY=your_openrouter_api_key
OPENAI_API_KEY=your_openai_api_key
LANGSMITH_TRACING=your_langsmith_tracing_value   # "true" 或 "false"
LANGSMITH_ENDPOINT=your_langsmith_endpoint
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=your_langsmith_project
PYTHONPATH=.
```

---

## **Quick Start**

### 1. 啟動 Telegram 前端

```bash
python3 telegram_frontend.py
```

機器人上線後，可在 Telegram 與 Bot 對話。

### 2. 啟動後端服務

```bash
cd agent/script/
python3 chatbot_tgram.py
```

## 更新 Chatbot 參數設定

位置：`agent/script/params.json`

模型與檢索設定：

* `emb_model`：Embedding 模型名稱
* `faiss_idx_path`：FAISS 索引路徑
* `k`：檢索筆數
* `chatbot_model`：聊天模型
* `judge_model`：評估模型
* `with_rag`：是否啟用 RAG
