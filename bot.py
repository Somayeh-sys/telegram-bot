!pip install pyTelegramBotAPI
import telebot

# ۱. توکن ربات تلگرام خود را اینجا بگذارید
TELEGRAM_TOKEN = "9113193987:AAEMQo4_0CJgX8xWXfqY9Rf1hv_7jBizvfw"

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

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_name = message.from_user.first_name or "دوست عزیز"
    user_text = message.text
    
    # پاسخ هوشمند و ساختاریافته‌ی محلی (بدون نیاز به اینترنت خارجی یا API)
    reply_text = (
        f"سلام {user_name} عزیز.\n"
        f"پیام شما با متن: «{user_text}» به دست من رسید.\n\n"
        "خانم رنجبر در اولین فرصت پس از بررسی پژوهشی، پیام شما را مطالعه و پاسخ خواهند داد."
    )
    
    bot.reply_to(message, reply_text)
    
    # (اختیاری) اگر خواستید می‌توانید پیام دریافتی را برای خودتان به عنوان ادمین هم فوروارد کنید
    # ADMIN_ID = 5640608870
    # bot.forward_message(ADMIN_ID, message.chat.id, message.id)

print("ربات پاسخگوی خودکارِ سمیه رنجبر روشن شد و آماده به کار است...")
bot.infinity_polling()
