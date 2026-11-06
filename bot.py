import telebot
import os

TELEGRAM_TOKEN = "9113193987:AAEMQo4_0CJgX8xWXfqY9Rf1hv_7jBizvfw"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "سلام! من دستیار هوشمندِ سمیه رنجبر (دانشجوی دکترای هوش مصنوعی) هستم.\n"
        "در حال حاضر ایشان مشغول پژوهش هستند. لطفاً پیام یا موضوع خود را بگذارید."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_text = message.text.lower()
    
    # پاسخ‌های هوشمندِ قاعده‌مند بر اساس کلمات کلیدی پیام کاربر
    if "سلام" in user_text or "درود" in user_text:
        reply = "سلام و درود! پیام شما دریافت شد. خانم رنجبر در اولین فرصت بررسی خواهند کرد."
    elif "پروژه" in user_text or "پژوهش" in user_text or "مقاله" in user_text:
        reply = "موضوع پژوهشی شما ثبت شد. توضیحات تکمیلی یا فایل‌های مربوطه را بفرستید تا به دست خانم رنجبر برسد."
    elif "قیمت" in user_text or "هزینه" in user_text:
        reply = "لطفاً جزئیات درخواست خود را مکتوب ارسال کنید تا بررسی شود."
    else:
        reply = f"پیام شما با متن («{message.text}») دریافت شد. خانم رنجبر پس از فراغت از کارهای پژوهشی پاسخ خواهند داد."
    
    bot.reply_to(message, reply)

print("ربات روشن است...")
bot.infinity_polling()
