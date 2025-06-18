main.py

import os import json import requests from flask import Flask, request from telebot import TeleBot, types from dotenv import load_dotenv from Manu_Baton import handle_menu_commands

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN") URL = os.getenv("WEBHOOK_URL")

bot = TeleBot(TOKEN) app = Flask(name)

Load supported languages

with open("lang_list.json", "r", encoding="utf-8") as f: SUPPORTED_LANGUAGES = json.load(f)

Language settings for users

user_settings = {}

Detect language

def detect_language(text): response = requests.post("https://libretranslate.com/detect", data={"q": text}) return response.json()[0]['language']

Translate text

def translate_text(text, target_lang, src_lang=None): data = {"q": text, "target": target_lang} if src_lang: data["source"] = src_lang response = requests.post("https://libretranslate.com/translate", data=data) return response.json().get("translatedText", "Translation error.")

Start command

@bot.message_handler(commands=["start"]) def send_welcome(message): bot.reply_to(message, "Welcome! I can translate your messages. Use /settings to configure.")

Menu commands

@bot.message_handler(commands=["settings", "auto", "contact", "donate", "about"]) def handle_menu(message): handle_menu_commands(bot, message)

Callback handler (for language settings)

@bot.callback_query_handler(func=lambda call: call.data.startswith("set_lang")) def callback_query(call): lang_code = call.data.split(":")[1] user_settings[str(call.from_user.id)] = {"target_lang": lang_code} bot.answer_callback_query(call.id, f"Language set to {SUPPORTED_LANGUAGES[lang_code]}.")

Handle text messages

@bot.message_handler(func=lambda message: True) def translate_message(message): user_id = str(message.from_user.id) settings = user_settings.get(user_id) if not settings: bot.reply_to(message, "Please use /settings to select your target language.") return

target = settings["target_lang"]
src = detect_language(message.text)

if src == target:
    bot.reply_to(message, "Source and target languages are the same.")
    return

translated = translate_text(message.text, target, src)
bot.reply_to(message, translated)

Webhook route

@app.route(f"/{TOKEN}", methods=["POST"]) def webhook(): bot.process_new_updates([types.Update.de_json(request.stream.read().decode("utf-8"))]) return "", 200

Set webhook

@app.route("/") def index(): bot.remove_webhook() bot.set_webhook(url=f"{URL}/{TOKEN}") return "Bot is running with webhook."

if name == "main": app.run(debug=False)

