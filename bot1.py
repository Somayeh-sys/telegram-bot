import os
import threading
import telebot
from telebot import types
from flask import Flask
import jdatetime

# توکن ربات تلگرام
BOT_TOKEN = "9113193987:AAFLP8sUWF6pIPiKsd8Fp9I_bSHhVY4Wo-M"

# شناسه عددی تلگرام شما برای دریافت اعلان‌ها
ADMIN_CHAT_ID = "5640608870"

# مشخصات حساب بانکی
CARD_NUMBER = "6219-8614-9142-6085"
CARD_HOLDER = "سمیه رنجبر"
TUITION_FEE = "تماس با مربی"

bot = telebot.TeleBot(BOT_TOKEN, threaded=True)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7!"

def notify_admin(user, action_text):
    if not ADMIN_CHAT_ID or ADMIN_CHAT_ID == "YOUR_TELEGRAM_NUMERIC_ID":
        return
    try:
        username = f"@{user.username}" if user.username else "ندارد"
        full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        now = jdatetime.datetime.now().strftime("%Y/%m/%d - %H:%M")
        
        msg = (
            f"🔔 **گزارش فعالیت جدید:**\n"
            f"👤 کاربر: {full_name}\n"
            f"🆔 یوزرنیم: {username}\n"
            f"⏰ زمان: {now}\n"
            f"📌 اقدام: {action_text}"
        )
        bot.send_message(ADMIN_CHAT_ID, msg, parse_mode="Markdown")
    except Exception as e:
        print(f"Error: {e}")

def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton("📄 راهنمایی مقاله", callback_data="paper_guide")
    b2 = types.InlineKeyboardButton("✍️ ویرایش مقاله", callback_data="paper_edit")
    b3 = types.InlineKeyboardButton("🥋 تایم باشگاه و ثبت‌نام", callback_data="gym_menu")
    b4 = types.InlineKeyboardButton("🎓 سوال دانشگاه آزاد", callback_data="azad_uni")
    b5 = types.InlineKeyboardButton("🛠 سوال ملی مهارت", callback_data="melli_uni")
    markup.add(b1, b2)
    markup.add(b3)
    markup.add(b4, b5)
    return markup

def gym_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton("⏰ مشاهده برنامه هفتگی سانس‌ها", callback_data="gym_schedule")
    b2 = types.InlineKeyboardButton("💳 پرداخت شهریه و ارسال فیش", callback_data="gym_payment")
    b_back = types.InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="main_menu")
    markup.add(b1, b2, b_back)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    notify_admin(message.from_user, "شروع ربات (/start)")
    text = (
        "سلام و درود! 🌸\n"
        "به دستیار ارتباطی **سمیه رنجبر** خوش آمدید.\n"
        "لطفاً گزینه‌ی مورد نظر خود را انتخاب فرمایید:"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user = call.from_user
    bot.answer_callback_query(call.id)
    
    if call.data == "main_menu":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="لطفاً یکی از گزینه‌های زیر را انتخاب فرمایید:",
            reply_markup=main_menu()
        )

    elif call.data == "paper_guide":
        notify_admin(user, "انتخاب: راهنمایی مقاله")
        ans = (
            "📚 **راهنمایی مقاله و امور پژوهشی:**\n\n"
            "مشاوره در زمینه‌های:\n"
            "- هوش مصنوعی، بینایی ماشین و یادگیری عمیق\n"
            "- انتخاب ژورنال و کنفرانس مناسب (ISI / Scopus)\n"
            "- ساختاربندی و ایده‌پردازی مقالات علمی\n\n"
            "لطفاً موضوع یا سوال پژوهشی خود را ارسال نمایید."
        )
        bot.send_message(call.message.chat.id, ans, parse_mode="Markdown")

    elif call.data == "paper_edit":
        notify_admin(user, "انتخاب: ویرایش مقاله")
        ans = (
            "✍️ **خدمات ویرایش مقاله:**\n\n"
            "- ویراستاری گرامری و نگارشی مقالات انگلیسی/فارسی\n"
            "- پارافریز و کاهش مشابهت متنی (Plagiarism)\n"
            "- تنظیم تمپلت و قالب مقالات\n\n"
            "لطفاً عنوان یا فایل خود را ارسال نمایید."
        )
        bot.send_message(call.message.chat.id, ans, parse_mode="Markdown")

    elif call.data == "gym_menu":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🥋 **بخش ورزش و باشگاه:**\nلطفاً گزینه‌ی مورد نظر را انتخاب فرمایید:",
            reply_markup=gym_menu(),
            parse_mode="Markdown"
        )

    elif call.data == "gym_schedule":
        notify_admin(user, "مشاهده سانس‌های باشگاه")
        schedule_text = (
            "🥋 **برنامه و زمان‌بندی سانس‌های باشگاه:**\n\n"
            "▫️ **کونگ‌فو بانوان:** روزهای فرد | ۱۶:۰۰ الی ۱۷:۳۰\n"
            "▫️ **ژیمناستیک مبتدی:** روزهای زوج | ۱۷:۰۰ الی ۱۸:۰۰\n"
            "▫️ **ژیمناستیک پیشرفته:** روزهای فرد | ۱۷:۳۰ الی ۱۸:۳۰\n"
            "▫️ **کونگ‌فو آقایان:** روزهای زوج | ۱۸:۰۰ الی ۲۰:۰۰\n"
            "▫️ **کونگ‌فو آقایان بزرگسال:** روزهای زوج | ۲۰:۰۰ الی ۲۱:۳۰\n"
            "▫️ **تکواندو:** روزهای زوج | ۱۵:۳۰ الی ۱۷:۰۰\n\n"
            "جهت واریز شهریه، دکمه‌ی «پرداخت شهریه و ارسال فیش» را انتخاب کنید."
        )
        bot.send_message(call.message.chat.id, schedule_text, parse_mode="Markdown")

    elif call.data == "gym_payment":
        notify_admin(user, "انتخاب: پرداخت شهریه")
        payment_info = (
            "💳 **اطلاعات واریز شهریه باشگاه:**\n\n"
            f"👤 به نام: **{CARD_HOLDER}**\n"
            f"💳 شماره کارت:\n`{CARD_NUMBER}`\n"
            f"💰 شهریه: **{TUITION_FEE}**\n\n"
            "⚠️ **مراحل ثبت‌نام:**\n"
            "۱. شهریه را به شماره کارت فوق واریز نمایید.\n"
            "۲. تصویر فیش واریزی را همراه با **نام کامل و رشته ورزشکار** در همین چت ارسال نمایید.\n"
            "پس از بررسی، تاییدیه ثبت‌نام برای شما ارسال می‌شود."
        )
        bot.send_message(call.message.chat.id, payment_info, parse_mode="Markdown")

    elif call.data == "azad_uni":
        notify_admin(user, "انتخاب: سوال دانشگاه آزاد")
        ans = (
            "🎓 **دانشجویان محترم دانشگاه آزاد اسلامی:**\n\n"
            "لطفاً سوال، نام درس و شماره دانشجویی خود را تایپ نمایید."
        )
        bot.send_message(call.message.chat.id, ans, parse_mode="Markdown")

    elif call.data == "melli_uni":
        notify_admin(user, "انتخاب: سوال دانشگاه ملی مهارت")
        ans = (
            "🛠 **دانشجویان گرامی دانشگاه ملی مهارت:**\n\n"
            "لطفاً سوال و عنوان درس خود را ارسال فرمایید تا پاسخ داده شود."
        )
        bot.send_message(call.message.chat.id, ans, parse_mode="Markdown")

@bot.message_handler(content_types=['photo'])
def handle_receipt_photo(message):
    notify_admin(message.from_user, "📸 ارسال عکس فیش")
    if ADMIN_CHAT_ID and ADMIN_CHAT_ID != "YOUR_TELEGRAM_NUMERIC_ID":
        try:
            caption = (
                f"💳 **فیش واریزی جدید دریافت شد!**\n"
                f"از طرف: {message.from_user.first_name} (@{message.from_user.username})\n"
                f"شناسه عددی: `{message.from_user.id}`"
            )
            bot.send_photo(ADMIN_CHAT_ID, message.photo[-1].file_id, caption=caption, parse_mode="Markdown")
        except Exception as e:
            print(f"Forward error: {e}")
            
    bot.reply_to(message, "✅ فیش واریزی شما با موفقیت دریافت شد و برای مربی/مدیر ارسال گردید. تشکر از شما! 🌸")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    notify_admin(message.from_user, f"متن پیام: {message.text}")
    bot.reply_to(message, "پیام شما دریافت شد. در اسرع وقت بررسی و پاسخ داده خواهد شد. 🌸")

# تابع اجرای سرور وب در پس‌زمینه برای اینکه رندر متوجه پورت شود
def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, use_reloader=False)

if __name__ == '__main__':
    # روشن کردن سرور وب در یک ترد جداگانه
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    # اجرای اصلی ربات تلگرام در پروسس اصلی
    print("Telegram Bot is starting polling...")
    bot.infinity_polling(skip_pending=True)
