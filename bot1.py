import telebot
import jdatetime

# ۱. توکن جدید شما
TELEGRAM_TOKEN = "9113193987:AAFAKaeh1nm0zmOlqrjak9qKIOugp2Bveqk"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "سلام! من دستیار هوشمندِ سمیه رنجبر (دانشجوی دکترای هوش مصنوعی) هستم.\n"
        "در حال حاضر ایشان مشغول پژوهش و کارهای دانشگاهی هستند. "
        "پیام شما دریافت شد و به ایشان اطلاع داده خواهد شد.\n\n"
        "لطفاً پیام، سوال یا موضوع خود را بگذارید."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    text = message.text.strip()
    
    # پاسخ به سوال تاریخ
    if "امروز چندم" in text or "تاریخ امروز" in text or "تاریخ" in text:
        today_jalali = jdatetime.date.today()
        months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
        month_name = months[today_jalali.month - 1]
        date_str = f"امروز {today_jalali.day} {month_name} سال {today_jalali.year} است."
        bot.reply_to(message, date_str)
    else:
        # پاسخ پیش‌فرض برای بقیه پیام‌ها
        bot.reply_to(message, "پیام شما دریافت شد. خانم رنجبر در اولین فرصت بررسی خواهند کرد.")

print("ربات روشن است...")
bot.infinity_polling()
