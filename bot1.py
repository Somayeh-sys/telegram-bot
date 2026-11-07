import os
import threading
from flask import Flask
import telebot
import jdatetime

# --- 1. وب‌سرور کوچک برای فریب دادن رندر و زنده ماندن ربات ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and running 24/7!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# اجرای وب‌سرور در پس‌زمینه
threading.Thread(target=run_web, daemon=True).start()

# --- 2. کدهای اصلی ربات تلگرام ---
TOKEN = "9113193987:AAFLP8sUWF6pIPiKsd8Fp9I_bSHhVY4Wo-M"  # اگر توکن جدید گرفتید، این توکن را جایگزین کنید
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "سلام! ربات فعال و آنلاین است. چطور می‌توانم کمکتان کنم؟")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text.lower() if message.text else ""
    
    if "امروز چندم" in text or "تاریخ" in text:
        today = jdatetime.date.today().strftime("%Y/%m/%d")
        bot.reply_to(message, f"امروز: {today}")
    elif "سلام" in text:
        bot.reply_to(message, "سلام، روزتون بخیر! پیام شما دریافت شد.")
    else:
        bot.reply_to(message, "پیام شما دریافت شد. در اسرع وقت پاسخ خواهم داد.")

print("Bot is polling...")
bot.infinity_polling()
