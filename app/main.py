from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.services.model import ask_model  # Import the ask_model function
import markdown
import os


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/static")

# --- Root Endpoint ---
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "response": ""})

# --- Chat Endpoint ---
@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, message: str = Form(...)):
    print(f"Received message: {message}")
    
    # Get the model's answer and convert it from Markdown to HTML.
    answer = ask_model(message)
    html_answer = markdown.markdown(answer)
    
    # Return the HTML page with the new model's response.
    return templates.TemplateResponse("index.html", {"request": request, "response": html_answer})
