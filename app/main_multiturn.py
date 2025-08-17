from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

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


# 重要：先宣告 /api* 路由；最後再 mount 前端
app.mount("/", StaticFiles(directory="app/static_site", html=True), name="frontend")
