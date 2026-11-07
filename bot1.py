import os
import threading
from flask import Flask
import telebot
from telebot import types
import jdatetime

TOKEN = "9113193987:AAFLP8sUWF6pIPiKsd8Fp9I_bSHhVY4Wo-M"
bot = telebot.TeleBot(TOKEN)

# ساخت کیبورد دکمه‌ها
def get_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("📄 راهنمایی مقاله", callback_data="paper_guide")
    btn2 = types.InlineKeyboardButton("✏️ ویرایش مقاله", callback_data="paper_edit")
    btn3 = types.InlineKeyboardButton("🏋️‍♂️ تایم باشگاه", callback_data="gym_time")
    btn4 = types.InlineKeyboardButton("🎓 سوال دانشگاه آزاد", callback_data="azad_univ")
    btn5 = types.InlineKeyboardButton("🛠 سوال ملی مهارت", callback_data="melli_maharat")
    
    markup.add(btn1, btn2)
    markup.add(btn3)
    markup.add(btn4, btn5)
    return markup

# دستور /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "سلام و درود! 🌸\n"
        "به ربات ارتباطی سمیه رنجبر خوش آمدید.\n\n"
        "لطفاً موضوع مورد نظر خود را از میان دکمه‌های زیر انتخاب فرمایید:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu())

# مدیریت کلیک روی دکمه‌ها
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "paper_guide":
        text = (
            "📌 **راهنمایی مقاله:**\n\n"
            "برای مشاوره و راهنمایی در نگارش مقالات علمی (هوش مصنوعی، بینایی ماشین، یادگیری عمیق):\n"
            "• موضوع، چکیده یا عنوان پیشنهادی خود را ارسال کنید.\n"
            "• مشخص بفرمایید هدف شما کنفرانس داخلی است یا ژورنال معتبر بین‌المللی (ISI/Scopus).\n"
            "در اسرع وقت بررسی شده و راهنمایی لازم خدمتتان ارسال خواهد شد."
        )
    elif call.data == "paper_edit":
        text = (
            "✏️ **ویرایش مقاله:**\n\n"
            "خدمات بازبینی و ادیت مقاله شامل:\n"
            "۱. اصلاح ساختار علمی و نگارشی متن انگلیسی/فارسی\n"
            "۲. کاهش مشابهت متنی و رفع درصد پلاجیاریسم (Plagiarism)\n"
            "۳. تنظیم دقیق فرمت بر اساس تمپلیت دانشگاه یا ژورنال هدف\n\n"
            "لطفاً فایل متنی را همراه با مشخصات ارسال نمایید."
        )
    elif call.data == "gym_time":
        text = (
            "🏋️‍♂️ **تایم باشگاه:**\n\n"
            "برنامه و سانس‌های ورزشی:\n"
            "• روزهای زوج: ۱۷:۰۰ الی ۱۹:۰۰\n"
            "• روزهای فرد: ۱۸:۰۰ الی ۲۰:۰۰\n\n"
            "در صورت تغییر در سانس‌ها یا هماهنگی ویژه، از همین طریق اطلاع‌رسانی می‌شود."
        )
    elif call.data == "azad_univ":
        text = (
            "🎓 **سوال درسی دانشگاه آزاد:**\n\n"
            "دانشجویان گرامی دانشگاه آزاد اسلامی:\n"
            "• لطفاً نام، نام خانوادگی، شماره دانشجویی و نام درس مربوطه را قید کنید.\n"
            "• سوال درسی یا فایل پروژه خود را ارسال نمایید.\n"
            "پاسخ‌ها در اولین فرصت کاری پس از بررسی ارسال خواهد شد."
        )
    elif call.data == "melli_maharat":
        text = (
            "🛠 **سوال درسی ملی مهارت:**\n\n"
            "دانشجویان گرامی دانشگاه ملی مهارت (فنی‌حرفه‌ای سابق):\n"
            "• لطفاً نام درس، عنوان پروژه/کارگاه و سوال مشخص خود را بفرمایید.\n"
            "• پروژه‌های عملی و کدها را به صورت فایل یا متن خوانا بفرستید.\n"
            "بررسی و پاسخ به نوبت خدمت شما ارسال می‌گردد."
        )
    else:
        text = "گزینه نامعتبر است."

    # پاسخ دادن به کاربر همراه با دکمه بازگشت به منو
    back_markup = types.InlineKeyboardMarkup()
    back_markup.add(types.InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="main_menu"))
    
    if call.data == "main_menu":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="لطفاً موضوع مورد نظر خود را انتخاب کنید:",
            reply_markup=get_main_menu()
        )
    else:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=back_markup,
            parse_mode="Markdown"
        )
    
    bot.answer_callback_query(call.id)

# پاسخ به پیام‌های متنی عادی
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text.lower() if message.text else ""
    
    if "امروز چندم" in text or "تاریخ" in text:
        today = jdatetime.date.today().strftime("%Y/%m/%d")
        bot.reply_to(message, f"📅 امروز: {today}")
    elif "سلام" in text or "درود" in text:
        bot.reply_to(message, "سلام، روزتون بخیر! لطفاً یکی از گزینه‌های منو را انتخاب کنید یا پیام خود را بنویسید:", reply_markup=get_main_menu())
    else:
        bot.reply_to(message, "پیام شما دریافت شد. در اسرع وقت پاسخ داده خواهد شد.\n\nبا احترام، سمیه رنجبر", reply_markup=get_main_menu())

# وب‌سرور برای زنده نگه‌داشتن روی رندر
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and running!"

def start_bot():
    print("Telegram Bot is polling...")
    bot.infinity_polling()

threading.Thread(target=start_bot, daemon=True).start()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
