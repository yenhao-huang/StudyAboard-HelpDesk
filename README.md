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
cd chatbot/app
uvicorn main:app --reload
```

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