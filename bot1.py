import os
import threading
import telebot
from telebot import types
from flask import Flask
import jdatetime

# ==================== تنظیمات اصلی ====================
# توکن ربات شما
BOT_TOKEN = "9113193987:AAFLP8sUWF6pIPiKsd8Fp9I_bSHhVY4Wo-M"

# آیدی عددی تلگرام خودتان (برای دریافت نوتیفیکیشن‌ها و فیش‌ها)
# از ربات @userinfobot در تلگرام بگیرید
ADMIN_CHAT_ID = "YOUR_TELEGRAM_NUMERIC_ID"  # مثلا: "123456789"

# اطلاعات کارت بانکی شما برای پرداخت شهریه
CARD_NUMBER = "6219-8614-9142-6085"
CARD_HOLDER = "سمیه رنجبر"
TUITION_FEE = "تماس / هماهنگی با مربی (700 هزار تومان)"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7!"

# تابع کمکی برای ارسال لاگ کاربری به پیوی شما
def notify_admin(user, action_text):
    try:
        username = f"@{user.username}" if user.username else "ندارد"
        full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        now = jdatetime.datetime.now().strftime("%Y/%m/%d - %H:%M")
        
        msg = (
            f"🔔 **گزارش فعالیت جدید:**\n"
            f"👤 کاربر: {full_name}\n"
            f"🆔 یوزرنیم: {username}\n"
            f"🔢 شناسه عددی: `{user.id}`\n"
            f"⏰ زمان: {now}\n"
            f"📌 اقدام: {action_text}"
        )
        bot.send_message(ADMIN_CHAT_ID, msg, parse_mode="Markdown")
    except Exception as e:
        print(f"Error notifying admin: {e}")

# منوی اصلی
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

# زیرمنوی باشگاه
def gym_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton("⏰ مشاهده برنامه هفتگی سانس‌ها", callback_data="gym_schedule")
    b2 = types.InlineKeyboardButton("💳 پرداخت شهریه و ارسال فیش", callback_data="gym_payment")
    b_back = types.InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="main_menu")
    markup.add(b1, b2, b_back)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    notify_admin(message.from_user, "شروع ربات (استارت)")
    text = (
        "سلام و درود! 🌸\n"
        "به دستیار ارتباطی **سمیه رنجبر** خوش آمدید.\n"
        "لطفاً گزینه‌ی مورد نظر خود را انتخاب فرمایید:"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user = call.from_user
    
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
            "- هوش مصنوعی، بینایی ماشین و یادگیری عمیق (Deep Learning)\n"
            "- انتخاب ژورنال و کنفرانس مناسب (ISI / Scopus)\n"
            "- ساختاربندی و ایده‌پردازی مقالات علمی\n\n"
            "لطفاً موضوع یا سوال پژوهشی خود را همین‌جا ارسال کنید تا بررسی و پاسخ داده شود."
        )
        bot.send_message(call.message.chat.id, ans, parse_mode="Markdown")

    elif call.data == "paper_edit":
        notify_admin(user, "انتخاب: ویرایش مقاله")
        ans = (
            "✍️ **خدمات ویرایش مقاله:**\n\n"
            "- ویراستاری گرامری و نگارشی مقالات انگلیسی/فارسی\n"
            "- پارافریز و کاهش تشابه متنی (Plagiarism / Turnitin)\n"
            "- قالب‌بندی طبق تمپلت ژورنال‌ها و کنفرانس‌ها\n\n"
            "لطفاً فایل یا عنوان مقاله خود را ارسال نمایید."
        )
        bot.send_message(call.message.chat.id, ans, parse_mode="Markdown")

    elif call.data == "gym_menu":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🥋 **بخش ورزش و باشگاه:**\nلطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=gym_menu(),
            parse_mode="Markdown"
        )

    elif call.data == "gym_schedule":
        notify_admin(user, "مشاهده: سانس‌های باشگاه")
        schedule_text = (
            "🥋 **برنامه و زمان‌بندی سانس‌های باشگاه:**\n\n"
            "▫️ **کونگ‌فو بانوان:** روزهای فرد | ساعت ۱۶:۰۰ الی ۱۷:۳۰\n"
            "▫️ **ژیمناستیک مبتدی:** روزهای زوج | ساعت ۱۷:۰۰ الی ۱۸:۰۰\n"
            "▫️ **ژیمناستیک پیشرفته:** روزهای فرد | ساعت ۱۷:۳۰ الی ۱۸:۳۰\n"
            "▫️ **کونگ‌فو آقایان:** روزهای زوج | ساعت ۱۸:۰۰ الی ۲۰:۰۰\n"
            "▫️ **کونگ‌فو آقایان بزرگسال:** روزهای زوج | ساعت ۲۰:۰۰ الی ۲۱:۳۰\n"
            "▫️ **تکواندو:** روزهای زوج | ساعت ۱۵:۳۰ الی ۱۷:۰۰\n\n"
            "جهت هماهنگی و واریز شهریه، از دکمه‌ی «پرداخت شهریه» استفاده نمایید."
        )
        bot.send_message(call.message.chat.id, schedule_text, parse_mode="Markdown")

    elif call.data == "gym_payment":
        notify_admin(user, "انتخاب: پرداخت شهریه باشگاه")
        payment_info = (
            "💳 **اطلاعات واریز شهریه باشگاه:**\n\n"
            f"👤 صاحب حساب: **{CARD_HOLDER}**\n"
            f"💳 شماره کارت:\n`{CARD_NUMBER}`\n"
            f"💰 شهریه: **{TUITION_FEE}**\n\n"
            "⚠️ **مراحل ثبت‌نام:**\n"
            "۱. مبلغ شهریه را به شماره کارت بالا واریز فرمایید.\n"
            "۲. تصویر فیش واریزی را به همراه **نام کامل ورزشکار** و **رشته ورزشی** به صورت عکس در همین چت ارسال نمایید.\n"
            "پس از تایید، ثبت‌نام نهایی به شما اعلام خواهد شد."
        )
        bot.send_message(call.message.chat.id, payment_info, parse_mode="Markdown")

    elif call.data == "azad_uni":
        notify_admin(user, "انتخاب: سوال دانشگاه آزاد")
        ans = (
            "🎓 **دانشجویان محترم دانشگاه آزاد اسلامی:**\n\n"
            "لطفاً سوال درسی، نام درس، شماره دانشجویی و مبحث مورد نظر خود را تایپ و ارسال کنید.\n"
            "در اولین فرصت پیام شما بررسی و پاسخ داده خواهد شد."
        )
        bot.send_message(call.message.chat.id, ans, parse_mode="Markdown")

    elif call.data == "melli_uni":
        notify_admin(user, "انتخاب: سوال دانشگاه ملی مهارت")
        ans = (
            "🛠 **دانشجویان گرامی دانشگاه ملی مهارت (فنی‌وحرفه‌ای سابق):**\n\n"
            "لطفاً نام درس، سرفصل و سوال آموزشی خود را ارسال فرمایید تا پیگیری شود."
        )
        bot.send_message(call.message.chat.id, ans, parse_mode="Markdown")

# دریافت عکس فیش واریزی یا مدارک و فوروارد به شما
@bot.message_handler(content_types=['photo'])
def handle_receipt_photo(message):
    notify_admin(message.from_user, "📸 ارسال عکس فیش واریزی یا مدرک")
    
    # ارسال عکس مستقیم به پیوی شما
    caption = (
        f"💳 **فیش واریزی جدید دریافت شد!**\n"
        f"از طرف: {message.from_user.first_name} (@{message.from_user.username})\n"
        f"شناسه کاربر: `{message.from_user.id}`"
    )
    bot.send_photo(ADMIN_CHAT_ID, message.photo[-1].file_id, caption=caption, parse_mode="Markdown")
    
    # پاسخ به کاربر
    bot.reply_to(message, "✅ فیش واریزی شما با موفقیت دریافت شد و برای مربی/مدیر ارسال گردید. پس از بررسی نتیجه به شما اعلام خواهد شد. تشکر از شما! 🌸")

# دریافت سایر پیام‌های متنی متفرقه کاربران
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    notify_admin(message.from_user, f"پیام متنی: {message.text}")
    bot.reply_to(message, "پیام شما دریافت شد. در اولین فرصت بررسی و به شما پاسخ داده خواهد شد. 🌸")

def run_telebot():
    bot.infinity_polling(skip_pending=True)

if __name__ == '__main__':
    t = threading.Thread(target=run_telebot)
    t.start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
