from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import pymysql
import os

BOT_TOKEN = os.getenv("8321912602:AAGy2xQxFAdo9pkSv55y6XCbo8Bu51ig-2c")
DB_HOST = os.getenv("mediumturquoise-hippopotamus-850998.hostingersite.com")
DB_USER = os.getenv("u817481458_iop")
DB_PASS = os.getenv("aJ$>XN^+O2")
DB_NAME = os.getenv("u817481458_3lmni")
CHANNEL = os.getenv("https://t.me/+Z0YdItTdbmZmYjc0")

def check_token_valid(token):
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT email FROM subscribers WHERE token = %s", (token,))
            return cursor.fetchone() is not None
    finally:
        conn.close()

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token = update.message.text.strip()
    if check_token_valid(token):
        await update.message.reply_text(f"✅ التوكن صحيح! ادخل القناة: {CHANNEL}")
    else:
        await update.message.reply_text("❌ توكن غير صحيح.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling()