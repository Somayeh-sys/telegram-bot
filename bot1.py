import os
import threading
from flask import Flask
import telebot
import jdatetime

# ۱. تعریف ربات تلگرام
TOKEN = "9113193987:AAFLP8sUWF6pIPiKsd8Fp9I_bSHhVY4Wo-M"  # مطمئن شوید همان توکن فعال است
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "سلام! ربات هوشمند فعال است. چطور می‌توانم کمکتان کنم؟")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text.lower() if message.text else ""
    
    # پاسخ به تاریخ
    if "امروز چندم" in text or "تاریخ" in text:
        today = jdatetime.date.today().strftime("%Y/%m/%d")
        bot.reply_to(message, f"📅 امروز: {today}")
        
    # پاسخ به وضعیت هوا
    elif "هوا" in text:
        bot.reply_to(message, "🌤 برای اطلاع دقیق از وضعیت آب‌وهوای شهرتان، لطفاً اپلیکیشن هواشناسی یا سایت هواشناسی استان را بررسی بفرمایید.")
        
    # پاسخ به سلام و احوال‌پرسی
    elif "سلام" in text or "درود" in text:
        bot.reply_to(message, "سلام! روزتون بخیر و شادی. در خدمتم.")
        
    # پاسخ پیش‌فرض به سایر پیام‌ها
    else:
        bot.reply_to(message, "پیام شما دریافت شد. در اسرع وقت بررسی و پاسخ داده خواهد شد. با احترام، سمیه رنجبر")

# ۲. اجرای پلینگ ربات تلگرام در ترد پس‌زمینه
def start_bot():
    print("Telegram Bot is polling...")
    bot.infinity_polling()

threading.Thread(target=start_bot, daemon=True).start()

# ۳. اجرای وب‌سرور در پیش‌زمینه تا رندر فورا پورت را شناسایی کند
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and running 24/7!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    print(f"Starting web server on port {port}...")
    app.run(host='0.0.0.0', port=port)
