import os
from dotenv import load_dotenv
load_dotenv()

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def comm_with_backend(user_text):
    print(f"Received message: {user_text}")

    shared_dir = "/tmp2/yenhao-llm/RAG-chatbot"
    w_path = shared_dir + "/msg.txt"
    r_path = shared_dir + "/msg2.txt"
    with open(w_path, "w") as f:
        f.write(user_text)
    
    # 等待回應
    while True:
        if os.path.exists(r_path):
            with open(r_path) as f:
                reply = f.read()
            if reply:  # 確保不是空字串
                break
    
    os.remove(r_path)
    print(reply)
    return reply

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! 我是你的 Telegram Bot 🤖")

async def close_rag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply = comm_with_backend(user_text)
    if reply == "Success":
        await update.message.reply_text("成功關閉 RAG")
    else:
        await update.message.reply_text("關閉 RAG 失敗")

async def open_rag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply = comm_with_backend(user_text)
    if reply == "Success":
        await update.message.reply_text("成功開啟 RAG")
    else:
        await update.message.reply_text("開啟 RAG 失敗")


async def chat_with_chatbot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply = comm_with_backend(user_text)
    await update.message.reply_text(reply)


app = Application.builder().token(TOKEN).build()

# "/start"
app.add_handler(CommandHandler("start", start))

# "/close_rag"
app.add_handler(CommandHandler("close_rag", close_rag))
app.add_handler(CommandHandler("open_rag", open_rag))
# Echo all text messages
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_chatbot))

app.run_polling()
