import os
import threading
import telebot
from telebot import types
from flask import Flask
import jdatetime

# ۱. توکن جدید دریافتی از BotFather را اینجا بگذارید
BOT_TOKEN = "9113193987:AAEs1L-35zKByrIi_fPzBdiUgj7MyJ0ZtmM"

# ۲. شناسه عددی تلگرام خودتان
ADMIN_CHAT_ID = "5640608870"

# مشخصات کارت بانکی
CARD_NUMBER = "6219-8614-9142-6085"
CARD_HOLDER = "سمیه رنجبر"
TUITION_FEE = "تماس با مربی"

bot = telebot.TeleBot(BOT_TOKEN, threaded=True)
app = Flask(__name__)

# ذخیره وضعیت موقت کاربران برای دریافت مرحله‌ای اطلاعات
user_states = {}

@app.route('/')
def home():
    return "Bot is running 24/7!"

def notify_admin(user, text_report):
    if not ADMIN_CHAT_ID or ADMIN_CHAT_ID == "YOUR_TELEGRAM_NUMERIC_ID":
        return
    try:
        username = f"@{user.username}" if user.username else "ندارد"
        full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        now = jdatetime.datetime.now().strftime("%Y/%m/%d - %H:%M")
        
        msg = (
            f"📩 **پیام / درخواست جدید دریافت شد:**\n"
            f"👤 ارسال‌کننده: {full_name}\n"
            f"🆔 یوزرنیم: {username}\n"
            f"🔢 شناسه عددی: `{user.id}`\n"
            f"⏰ زمان: {now}\n"
            f"──────────────────\n"
            f"{text_report}"
        )
        bot.send_message(ADMIN_CHAT_ID, msg, parse_mode="Markdown")
    except Exception as e:
        print(f"Error in notify_admin: {e}")

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

# دکمه بازگشت ساده به منوی اصلی
def back_button():
    markup = types.InlineKeyboardMarkup()
    b_back = types.InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="main_menu")
    markup.add(b_back)
    return markup

# زیرمنوی باشگاه
def gym_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton("⏰ برنامه هفتگی سانس‌ها", callback_data="gym_schedule")
    b2 = types.InlineKeyboardButton("💳 پرداخت شهریه و ثبت‌نام", callback_data="gym_payment")
    b_back = types.InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="main_menu")
    markup.add(b1, b2, b_back)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_states.pop(message.chat.id, None)
    text = (
        "سلام و درود! 🌸\n\n"
        "به سیستم ارتباطی و مشاوره‌ای **سمیه رنجبر** خوش آمدید.\n"
        "لطفاً خدمت یا بخش مورد نظر خود را از گزینه‌های زیر انتخاب نمایید:"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    user = call.from_user
    bot.answer_callback_query(call.id)
    
    if call.data == "main_menu":
        user_states.pop(chat_id, None)
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=call.message.message_id,
                text="لطفاً یکی از گزینه‌های زیر را انتخاب فرمایید:",
                reply_markup=main_menu()
            )
        except Exception:
            bot.send_message(chat_id, "لطفاً یکی از گزینه‌های زیر را انتخاب فرمایید:", reply_markup=main_menu())

    elif call.data == "paper_guide":
        user_states[chat_id] = 'awaiting_paper_guide'
        msg = (
            "📚 **بخش راهنمایی و مشاوره مقاله:**\n\n"
            "لطفاً اطلاعات زیر را در **یک پیام** ارسال فرمایید:\n"
            "۱. نام و نام خانوادگی\n"
            "۲. رشته و مقطع تحصیلی\n"
            "۳. عنوان یا ایده مقاله و سوال پژوهشی شما\n\n"
            "👇 پیام خود را تایپ و ارسال کنید:"
        )
        bot.send_message(chat_id, msg, reply_markup=back_button(), parse_mode="Markdown")

    elif call.data == "paper_edit":
        user_states[chat_id] = 'awaiting_paper_edit'
        msg = (
            "✍️ **بخش ویراستاری و اصلاح مقاله:**\n\n"
            "لطفاً اطلاعات زیر را در **یک پیام** بنویسید (یا فایل مقاله را با متن توضیحات بفرستید):\n"
            "۱. نام و نام خانوادگی\n"
            "۲. مقطع تحصیلی و رشته\n"
            "۳. عنوان مقاله\n"
            "۴. نوع ویرایش مدنظر (نگارشی، پارافریز، قالب‌بندی مجله و...)\n\n"
            "👇 مشخصات را ارسال بفرمایید:"
        )
        bot.send_message(chat_id, msg, reply_markup=back_button(), parse_mode="Markdown")

    elif call.data == "gym_menu":
        user_states.pop(chat_id, None)
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=call.message.message_id,
                text="🥋 **بخش ورزش و باشگاه:**\nلطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
                reply_markup=gym_menu(),
                parse_mode="Markdown"
            )
        except Exception:
            bot.send_message(chat_id, "🥋 **بخش ورزش و باشگاه:**\nلطفاً گزینه‌ی مورد نظر را انتخاب فرمایید:", reply_markup=gym_menu(), parse_mode="Markdown")

    elif call.data == "gym_schedule":
        schedule_text = (
            "🥋 **برنامه و زمان‌بندی سانس‌های باشگاه:**\n\n"
            "▫️ **کونگ‌فو بانوان:** روزهای فرد | ۱۶:۰۰ الی ۱۷:۳۰\n"
            "▫️ **ژیمناستیک مبتدی:** روزهای زوج | ۱۷:۰۰ الی ۱۸:۰۰\n"
            "▫️ **ژیمناستیک پیشرفته:** روزهای فرد | ۱۷:۳۰ الی ۱۸:۳۰\n"
            "▫️ **کونگ‌فو آقایان:** روزهای زوج | ۱۸:۰۰ الی ۲۰:۰۰\n"
            "▫️ **کونگ‌فو آقایان بزرگسال:** روزهای زوج | ۲۰:۰۰ الی ۲۱:۳۰\n"
            "▫️ **تکواندو:** روزهای زوج | ۱۵:۳۰ الی ۱۷:۰۰\n\n"
            "جهت واریز و نهایی کردن ثبت‌نام، روی دکمه زیر بزنید یا به منوی قبل بازگردید:"
        )
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("💳 پرداخت شهریه و ثبت‌نام", callback_data="gym_payment"),
            types.InlineKeyboardButton("🔙 بازگشت به منوی باشگاه", callback_data="gym_menu")
        )
        bot.send_message(chat_id, schedule_text, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "gym_payment":
        user_states[chat_id] = 'awaiting_gym_reg'
        payment_info = (
            "💳 **اطلاعات واریز و ثبت‌نام باشگاه:**\n\n"
            f"👤 به نام: **{CARD_HOLDER}**\n"
            f"💳 شماره کارت:\n`{CARD_NUMBER}`\n"
            f"💰 شهریه: **{TUITION_FEE}**\n\n"
            "📌 **جهت تکمیل ثبت‌نام:**\n"
            "لطفاً **نام و نام خانوادگی ورزشکار، سن و رشته ورزشی** را بنویسید و همراه با **عکس فیش واریزی** در همین چت ارسال نمایید."
        )
        bot.send_message(chat_id, payment_info, reply_markup=back_button(), parse_mode="Markdown")

    elif call.data == "azad_uni":
        user_states[chat_id] = 'awaiting_azad_uni'
        ans = (
            "🎓 **دانشجویان گرامی دانشگاه آزاد اسلامی:**\n\n"
            "لطفاً در یک پیام موارد زیر را بنویسید:\n"
            "۱. نام و نام خانوادگی\n"
            "۲. شماره دانشجویی\n"
            "۳. عنوان درس\n"
            "۴. سوال یا موضوع مورد نظر\n\n"
            "👇 پیام خود را بفرستید:"
        )
        bot.send_message(chat_id, ans, reply_markup=back_button(), parse_mode="Markdown")

    elif call.data == "melli_uni":
        user_states[chat_id] = 'awaiting_melli_uni'
        ans = (
            "🛠 **دانشجویان گرامی دانشگاه ملی مهارت:**\n\n"
            "لطفاً موارد زیر را در یک پیام بفرستید:\n"
            "۱. نام و نام خانوادگی\n"
            "۲. شماره دانشجویی\n"
            "۳. عنوان درس\n"
            "۴. شرح سوال شما\n\n"
            "👇 پیام خود را ارسال بفرمایید:"
        )
        bot.send_message(chat_id, ans, reply_markup=back_button(), parse_mode="Markdown")

# مدیریت ارسال عکس (مثل فیش بانکی)
@bot.message_handler(content_types=['photo'])
def handle_receipt_photo(message):
    chat_id = message.chat.id
    caption = message.caption or "بدون توضیحات متنی"
    user_state = user_states.get(chat_id, 'gym_payment_photo')
    
    report_title = "📸 **فیش واریزی / تصویر ارسالی**"
    if user_state == 'awaiting_gym_reg':
        report_title = "🥋 **ثبت‌نام جدید باشگاه + تصویر فیش**"

    if ADMIN_CHAT_ID and ADMIN_CHAT_ID != "YOUR_TELEGRAM_NUMERIC_ID":
        try:
            admin_caption = (
                f"{report_title}\n"
                f"👤 از طرف: {message.from_user.first_name or ''} {message.from_user.last_name or ''}\n"
                f"🆔 یوزرنیم: @{message.from_user.username or 'ندارد'}\n"
                f"🔢 شناسه: `{message.from_user.id}`\n"
                f"📝 متن همراه عکس: {caption}"
            )
            bot.send_photo(ADMIN_CHAT_ID, message.photo[-1].file_id, caption=admin_caption, parse_mode="Markdown")
        except Exception as e:
            print(f"Error forwarding photo: {e}")
            
    bot.reply_to(
        message, 
        "✅ تصویر و اطلاعات شما با موفقیت ثبت شد و برای استاد/مربی ارسال گردید. سپاس از شما! 🌸", 
        reply_markup=main_menu()
    )
    user_states.pop(chat_id, None)

# مدیریت ارسال فایل سندی (مانند فایل Word یا PDF مقاله)
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    chat_id = message.chat.id
    doc_caption = message.caption or "بدون توضیحات"
    
    if ADMIN_CHAT_ID and ADMIN_CHAT_ID != "YOUR_TELEGRAM_NUMERIC_ID":
        try:
            admin_caption = (
                f"📁 **فایل مقاله جدید دریافت شد**\n"
                f"👤 کاربر: {message.from_user.first_name or ''} {message.from_user.last_name or ''}\n"
                f"🆔 @{message.from_user.username or 'ندارد'}\n"
                f"📝 توضیحات: {doc_caption}"
            )
            bot.send_document(ADMIN_CHAT_ID, message.document.file_id, caption=admin_caption, parse_mode="Markdown")
        except Exception as e:
            print(f"Error doc: {e}")

    bot.reply_to(
        message,
        "✅ فایل ارسالی شما با موفقیت دریافت و تحویل داده شد. به زودی بررسی خواهد شد. 🌸",
        reply_markup=main_menu()
    )
    user_states.pop(chat_id, None)

# دریافت و ثبت پیام‌های متنی بر اساس بخش انتخابی
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    chat_id = message.chat.id
    state = user_states.get(chat_id)
    text = message.text

    if state == 'awaiting_paper_guide':
        report = f"📄 **درخواست راهنمایی مقاله:**\n{text}"
        notify_admin(message.from_user, report)
        reply = "✅ مشخصات و عنوان مقاله شما دریافت شد. در اسرع وقت بررسی و راهنمایی لازم ارائه خواهد شد. 🌸"
        user_states.pop(chat_id, None)

    elif state == 'awaiting_paper_edit':
        report = f"✍️ **درخواست ویرایش مقاله:**\n{text}"
        notify_admin(message.from_user, report)
        reply = "✅ اطلاعات مقاله ویرایشی شما ثبت گردید. جهت هماهنگی بررسی خواهد شد. 🌸"
        user_states.pop(chat_id, None)

    elif state == 'awaiting_gym_reg':
        report = f"🥋 **اطلاعات ثبت‌نام باشگاه:**\n{text}"
        notify_admin(message.from_user, report)
        reply = "✅ اطلاعات شما ثبت شد. لطفاً تصویر فیش واریزی را نیز ارسال فرمایید. 🌸"

    elif state == 'awaiting_azad_uni':
        report = f"🎓 **سوال دانشجوی دانشگاه آزاد:**\n{text}"
        notify_admin(message.from_user, report)
        reply = "✅ سوال شما دریافت گردید و پس از بررسی پاسخ داده خواهد شد. 🌸"
        user_states.pop(chat_id, None)

    elif state == 'awaiting_melli_uni':
        report = f"🛠 **سوال دانشجوی دانشگاه ملی مهارت:**\n{text}"
        notify_admin(message.from_user, report)
        reply = "✅ سوال شما دریافت گردید و بررسی خواهد شد. 🌸"
        user_states.pop(chat_id, None)

    else:
        # پیام عمومی
        notify_admin(message.from_user, f"💬 **پیام متفرقه:**\n{text}")
        reply = "پیام شما دریافت شد. در صورت تمایل می‌توانید از منوی زیر بخش مورد نظر خود را انتخاب نمایید: 🌸"

    bot.reply_to(message, reply, reply_markup=main_menu())

# سرور وب برای Render
def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, use_reloader=False)

if __name__ == '__main__':
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    print("Telegram Bot is running with interactive states...")
    bot.infinity_polling(skip_pending=True)
