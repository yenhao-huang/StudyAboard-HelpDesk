from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.request import HTTPXRequest

def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update.message.reply_text(f"Hello {update.effective_user.first_name}")

# 強制使用 httpx 作為 request backend
request = HTTPXRequest()
app = ApplicationBuilder().token("7635197948:AAGWxt2nEiPqZMvxFwEWlykfxBqCIisFuOA").request(request).build()
app.add_handler(CommandHandler("hello", hello))
app.run_polling()
