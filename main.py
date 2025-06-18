import os
import json
import requests
from flask import Flask, request
import telebot
from telebot import types

# Load supported languages from lang_list.json
with open("lang_list.json", "r", encoding="utf-8") as f:
    SUPPORTED_LANGUAGES = json.load(f)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not BOT_TOKEN:
    raise Exception("TELEGRAM_BOT_TOKEN environment variable missing!")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)
user_settings = {}

def translate_text(text, target_lang, src_lang=None):
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": src_lang or "auto",
        "tl": target_lang,
        "dt": "t",
        "q": text,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        try:
            result = response.json()
            return result[0][0][0]
        except Exception:
            return "❗ অনুবাদে সমস্যা হয়েছে"
    return "❗ অনুবাদে সমস্যা হয়েছে"

def detect_language(text):
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": "auto",
        "tl": "en",
        "dt": "t",
        "q": text,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        try:
            result = response.json()
            return result[2]
        except Exception:
            return None
    return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("🌐 ভাষা ও মোড পরিবর্তন করুন"),
        types.KeyboardButton("👨‍💻 ডেভেলপারকে যোগাযোগ করুন"),
        types.KeyboardButton("☕️ ডোনেট")
    )
    bot.send_message(
        message.chat.id,
        "👋 স্বাগতম!\n\nএই বটটি গ্রুপে স্বয়ংক্রিয় অনুবাদ করবে।\nশুরু করতে গ্রুপে অ্যাড করে অ্যাডমিন দিন।",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == "🌐 ভাষা ও মোড পরিবর্তন করুন")
def language_mode_menu(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ প্রধান ভাষা", callback_data="main_language"),
        types.InlineKeyboardButton("✅ দ্বিতীয় ভাষা", callback_data="second_language"),
        types.InlineKeyboardButton("🤖 অটো মোড", callback_data="auto_mode")
    )
    bot.send_message(message.chat.id, "ভাষা বা মোড পরিবর্তনের জন্য অপশন বেছে নিন:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "👨‍💻 ডেভেলপারকে যোগাযোগ করুন")
def contact_developer(message):
    text = (
        "নিউজ চ্যানেল: @BD_Translate\n"
        "কমিউনিটি: @BDTranslate_support\n"
        "Airdrop Channel: @latest_airdrop24\n"
        "ডেভেলপার: @nknoman22"
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text == "☕️ ডোনেট")
def donate_info(message):
    text = (
        "আপনি ক্রিপ্টোতে ডোনেট দিয়ে ডেভেলপমেন্টে উৎসাহ দিতে পারেন:\n\n"
        "TON: `UQDp1CVncTjyjtN_2Iu8rKgwRIcIp3XoJis8Jl88pLbkql4M`\n"
        "BTC: `bc1parq4cl9d2cu0k59tndvxxdjxtk74kde35hp35pevn35e588tue4sqlv4x4`\n"
        "ETH/USDT ERC20: `0x56C889b818c13955070f83D396b33A6a25eFA7CB`\n"
        "BNB/USDT BEP20: `0x56C889b818c13955070f83D396b33A6a25eFA7CB`\n"
        "SOL: `Hgo1rXUqzGpXriRsjVGWgAuv6Ag77XnfU48TdUF3aFwy`\n"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data in ["main_language", "second_language", "auto_mode"])
def set_language_callback(call):
    group_id = call.message.chat.id
    cb = call.data
    lang_markup = types.InlineKeyboardMarkup(row_width=2)
    for code, name in SUPPORTED_LANGUAGES.items():
        lang_markup.add(types.InlineKeyboardButton(name, callback_data=f"{cb}:{code}"))
    bot.edit_message_text("ভাষা নির্বাচন করুন:", group_id, call.message.message_id, reply_markup=lang_markup)

@bot.callback_query_handler(func=lambda call: any(call.data.startswith(prefix) for prefix in ["main_language:", "second_language:", "auto_mode:"]))
def save_language(call):
    group_id = call.message.chat.id
    user_settings.setdefault(group_id, {"main": None, "second": None, "auto": None})
    prefix, lang_code = call.data.split(":")
    lang_name = SUPPORTED_LANGUAGES.get(lang_code, lang_code)
    if prefix == "main_language":
        user_settings[group_id]["main"] = lang_code
        bot.edit_message_text(f"✅ প্রধান ভাষা সেট হয়েছে: {lang_name}", group_id, call.message.message_id)
    elif prefix == "second_language":
        user_settings[group_id]["second"] = lang_code
        bot.edit_message_text(f"✅ দ্বিতীয় ভাষা সেট হয়েছে: {lang_name}", group_id, call.message.message_id)
    elif prefix == "auto_mode":
        user_settings[group_id]["auto"] = lang_code
        bot.edit_message_text(f"✅ অটো মোড ভাষা: {lang_name}", group_id, call.message.message_id)

@bot.message_handler(func=lambda m: m.chat.type in ["group", "supergroup"] and not m.text.startswith("/"))
def group_translate(message):
    group_id = message.chat.id
    if group_id not in user_settings:
        return
    settings = user_settings[group_id]
    src_text = message.text
    detected_lang = detect_language(src_text)
    main = settings.get("main")
    second = settings.get("second")
    auto = settings.get("auto")
    if main and second and not auto:
        if detected_lang == main and detected_lang != second:
            translated = translate_text(src_text, second, main)
            bot.reply_to(message, f"💬 {SUPPORTED_LANGUAGES[second]}: {translated}")
        elif detected_lang == second and detected_lang != main:
            translated = translate_text(src_text, main, second)
            bot.reply_to(message, f"💬 {SUPPORTED_LANGUAGES[main]}: {translated}")
    elif auto:
        if detected_lang and detected_lang != auto and detected_lang in SUPPORTED_LANGUAGES.keys():
            translated = translate_text(src_text, auto, detected_lang)
            bot.reply_to(message, f"💬 {SUPPORTED_LANGUAGES[auto]}: {translated}")

# Webhook route
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    return '', 403

# Root check route
@app.route("/", methods=["GET"])
def index():
    return "Bot is running via webhook!", 200

# Set webhook if run directly
if __name__ == "__main__":
    if WEBHOOK_URL:
        bot.remove_webhook()
        bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))