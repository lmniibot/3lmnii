from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import pymysql
import os

# قراءة المتغيرات من البيئة (Secrets)
BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
CHANNEL = os.getenv("CHANNEL")

# دالة التحقق من التوكن في قاعدة البيانات
def check_token_valid(token):
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT email FROM subscribers WHERE token = %s", (token,))
            return cursor.fetchone() is not None
    finally:
        conn.close()

# التعامل مع الرسائل النصية
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token = update.message.text.strip()
    if check_token_valid(token):
        await update.message.reply_text(
            f"✅ التوكن صحيح!\nاضغط هنا للدخول إلى القناة: 👉 {CHANNEL}"
        )
    else:
        await update.message.reply_text("❌ التوكن غير صحيح. تأكد أنك نسخته بشكل صحيح.")

# إعداد البوت وتشغيله
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling()
