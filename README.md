```
├── app/
│   ├── main.py                  # FastAPI / Flask app 主程式
│   ├── api/                     # 放 API route (如 /chat)
│   │   └── routes.py
│   ├── services/                # 模型邏輯，如 chat、embedding 等
│   │   └── model.py
│   ├── templates/               # HTML 模板
│   │   └── index.html
│   ├── static/                  # JS / CSS / 圖片 等靜態資源
│   └── utils/                   # 共用工具（logger, validator 等）
│       └── helpers.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```
## How to Use
```
cd chatbot
uvicorn app.main:app --reload
```
### Chatbot 參數設定
file: app.services.model.py

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

## Techniques
### FastAPI
HTML rendering (read HTML files)
```
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
```

Input: Request; Ouput: `templates.TemplateResponse`

Get v.s. Post request
>Get: read; Post: 傳遞表單