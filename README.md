# RAG-CHATBOT

本專案是一個基於 Retrieval-Augmented Generation (RAG) 的**留學代辦客服系統**，整合 LLM API、後端服務與前端介面，協助用戶快速獲取正確資訊，並解決地域性問題造成的幻覺。

* **結果**
  * Retrieval: **Precision\@5 = 85.5%**
  * Generation:

<video src="metadata/rag_chabot.mp4" controls width="600"></video>
---

## Project Structure

```
RAG-CHATBOT/
├── agent/         # LLM + RAG API
├── app/           # 後端服務 (FastAPI)
├── frontend/      # 前端介面
├── tutorial/      # RAG 練習與範例
├── .env           # 環境變數
├── .gitignore     # 忽略檔案設定
└── README.md      # 專案說明文件
```

---

## How to Use

啟動後端服務：

```bash
cd chatbot
uvicorn app.main:app --reload
```

---

## Chatbot 參數設定

位置：`app/services/model.py`
透過 `ChatbotParams` 集中管理模型與檢索設定：

* `emb_model`：Embedding 模型名稱
* `faiss_idx_path`：FAISS 索引路徑
* `k`：檢索筆數
* `chatbot_model`：聊天模型
* `judge_model`：評估模型
* `with_rag`：是否啟用 RAG

**內建三組參數**：

1. `PARAMS_ALIBABA_WORAG` — Alibaba Embedding，關閉 RAG（純生成）
2. `PARAMS_ALIBABA` — Alibaba Embedding，啟用 RAG
3. `PARAMS_SENTENCE` — Sentence-Transformers Embedding（英文優化），啟用 RAG

---

## Techniques

### FastAPI — HTML Rendering

```python
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
```

* **Input**: `Request`
* **Output**: `templates.TemplateResponse`

### Get v.s. Post

* **GET**：讀取資料
* **POST**：傳遞表單