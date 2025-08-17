太好了！下面用「一步一步」帶你從零到一：建後端、建前端、接起來、最後把兩者合併成同一個服務。

---

# 1) 後端（FastAPI）— 建置與啟動

**(1) 建環境與安裝套件**

```bash
# 建議在專案根目錄
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install fastapi uvicorn pydantic[dotenv] markdown
```

**(2) 建目錄結構**

```
backend/
  app/
    __init__.py
    main.py
    services/
      __init__.py
      model.py
```

**(3) 建立最小可用的模型函式（先用假資料模擬）**
`backend/app/services/model.py`

```python
# 這裡先用簡單函式模擬模型回覆；之後你可改連真正的 LLM
def ask_model(prompt: str) -> str:
    return f"（模型回覆）你剛剛說：{prompt}"
```

**(4) 建立 API：非串流 / 串流（SSE）**
`backend/app/main.py`

```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import List, Literal
import asyncio

from app.services.model import ask_model

app = FastAPI()

# 開發時先寬鬆一點，部署時請收斂 allow_origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

class Msg(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

class ChatPayload(BaseModel):
    messages: List[Msg]

@app.post("/api/chat")
async def chat_json(payload: ChatPayload):
    """非串流：回傳完整字串"""
    last_user = next((m for m in reversed(payload.messages) if m.role == "user"), None)
    prompt = last_user.content if last_user else ""
    text = ask_model(prompt)
    return JSONResponse({"reply": text})

@app.post("/api/chat/stream")
async def chat_stream(request: Request, payload: ChatPayload):
    """串流：SSE，以 data: <token> 逐行回傳"""
    async def event_generator():
        last_user = next((m for m in reversed(payload.messages) if m.role == "user"), None)
        prompt = last_user.content if last_user else ""
        full = ask_model(prompt)

        for ch in full:  # 真正串流時，改成 async for token in your_model_stream(...):
            if await request.is_disconnected():
                break
            yield f"data:{ch}\n\n"
            await asyncio.sleep(0.005)  # 模擬打字速度

        yield "data:[DONE]\n\n"

    headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no",  # Nginx 如有反代，避免緩衝
    }
    return StreamingResponse(event_generator(), media_type="text/event-stream", headers=headers)
```

**(5) 啟動後端**

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

測試：

* 非串流：`POST http://127.0.0.1:8000/api/chat`
* 串流：`POST http://127.0.0.1:8000/api/chat/stream`（需用前端或 curl 讀取串流）

---

# 2) 前端（React + Vite + Tailwind）— 建置與啟動

**(1) 建專案**

```bash
# 回到專案根目錄
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
```

**(2) 安裝 Tailwind**

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

修改 `tailwind.config.js`：

```js
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: { extend: {} },
  plugins: [],
}
```

在 `src/index.css` 開頭加入：

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**(3) 安裝 icon 套件（和我給你的 UI 相同）**

```bash
npm install lucide-react
```

**(4) 加入你要的 Chat UI 元件**
在 `frontend/src/MultiTurnChat.tsx` 新增檔案，**把我先前給你的「Multi-Turn Chatbot UI (React)」整段程式碼貼進去**（你已經在 Canvas 看得到了）。

**(5) 寫好 provider（如何呼叫後端）**
在 `frontend/src/providers.ts` 新增：

```ts
export type Role = "system" | "user" | "assistant";
export type ChatMessage = { role: Role; content: string };

export const simpleProvider = async (history: ChatMessage[], { signal }: { signal?: AbortSignal } = {}) => {
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages: history }),
    signal,
  });
  const json = await res.json();
  return json.reply as string;
};

export const sseProvider = async function* (history: ChatMessage[], { signal }: { signal?: AbortSignal } = {}) {
  const res = await fetch("/api/chat/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages: history }),
    signal,
  });
  const reader = res.body!.getReader();
  const dec = new TextDecoder();
  let buffer = "";
  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += dec.decode(value, { stream: true });
    const parts = buffer.split("\n\n");
    buffer = parts.pop() || "";
    for (const chunk of parts) {
      if (!chunk.startsWith("data:")) continue;
      const data = chunk.slice(5).trim();
      if (data === "[DONE]") return;
      yield data;
    }
  }
};
```

**(6) 把 UI 擺進 App**
`frontend/src/App.tsx`

```tsx
import MultiTurnChat from "./MultiTurnChat";
import { sseProvider } from "./providers"; // 或改用 simpleProvider

export default function App() {
  return <MultiTurnChat chatProvider={sseProvider} />;
}
```

**(7) 開發時的 API 代理（避免 CORS）**
`frontend/vite.config.ts`

```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": "http://127.0.0.1:8000",
    },
  },
})
```

**(8) 啟動前端**

```bash
npm run dev
```

此時瀏覽器開 `http://localhost:5173`，前端會把 `/api/*` 代理到 `http://127.0.0.1:8000/api/*`，你就可以開始多輪對話了。

---

# 3) 兩者「合併」成同一個服務（部署）

開發時前後端分開跑比較舒服；**部署**時常把前端打包後由 FastAPI 直接提供。

**(1) 前端打包**

```bash
cd frontend
npm run build
# 會產生 frontend/dist
```

**(2) 後端掛載打包好的靜態檔**
把 `frontend/dist` 放在 `backend/` 同層或裡面都可以。以下假設你把 `frontend/dist` 複製到 `backend/static_site`。

```bash
# 例：在專案根目錄
cp -r frontend/dist backend/static_site
```

修改 `backend/app/main.py`（加在檔尾，/api 路由上方的程式保持不變）：

```python
from fastapi.staticfiles import StaticFiles

# 重要：先宣告 /api* 路由；最後再 mount 前端
app.mount("/", StaticFiles(directory="static_site", html=True), name="frontend")
```

**(3) 啟動**

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

現在打 `http://<server>:8000/` 就能看到前端，且 `/api/*` 由同一個 FastAPI 服務處理。

---

# 4) 你可能會遇到的常見問題

* **CORS 錯誤**：開發時請使用 Vite 的 `server.proxy`，或在 FastAPI 的 CORSMiddleware 指定你的前端網址。
* **SSE 被 Nginx 緩衝**：反向代理時加上 `proxy_buffering off;`，或像上面在 Header 用 `X-Accel-Buffering: no`。
* **POST + SSE**：瀏覽器的 `EventSource` 只支援 GET，**請用 `fetch()`** 讀取 `ReadableStream`（我們的做法就是）。
* **Abort 停止**：UI 會傳 `AbortSignal`，後端用 `await request.is_disconnected()` 中止串流。
* **System Prompt**：UI 會把 system 訊息放在 `messages` 裡（role=`system`），後端若需要可自行讀取第一則。

---

# 5) 接下來要做什麼？

* 你可以先把 Canvas 裡的 `MultiTurnChat` 直接複製到 `frontend/src/MultiTurnChat.tsx`。
* 如果你要把你現有的 `/chat`（回傳 HTML）保留也沒問題；React 端只用 `/api/chat` 與 `/api/chat/stream`。
* 如果你把你的真正 `ask_model(...)` 介面或串流寫法貼上來，我可以幫你把 **SSE 串流** 改到可直接用在你的模型上。
