import os
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()

# Set up OpenAI client
openai_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Telegram bot token
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# /start 指令
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your bot. Type anything and I'll echo it.")


# Handler for incoming text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_query = update.message.text
    print(f"Received message: {user_query}")

    prompt = f"""Context:
    N/A

    Question:
    {user_query}

    Answer:
    """

    try:
        response = openai_client.chat.completions.create(
            model="qwen/qwen3-coder:free",
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        answer = f"Error: {e}"

    await update.message.reply_text(answer)

# Start the bot
if __name__ == "__main__":
    # build bot
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    # start
    app.add_handler(CommandHandler("start", start))
    # response
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot is running...")
    app.run_polling()
