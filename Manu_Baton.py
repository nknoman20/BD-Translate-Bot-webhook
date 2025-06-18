# Manu_Baton.py

from telebot import types
import json

def handle_settings(bot, message, supported_languages, user_settings):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Main Language", callback_data="main_language"),
        types.InlineKeyboardButton("Second Language", callback_data="second_language"),
    )
    bot.send_message(message.chat.id, "Select your preferred language:", reply_markup=markup)

def handle_auto(bot, message, supported_languages, user_settings):
    markup = types.InlineKeyboardMarkup()
    for code, name in supported_languages.items():
        markup.add(types.InlineKeyboardButton(name, callback_data=f"auto_mode:{code}"))
    bot.send_message(message.chat.id, "Select language for Auto Mode:", reply_markup=markup)

def handle_contact(bot, message):
    text = (
        "👨‍💻 Developer Contact:\n"
        "Telegram: @nknoman22\n"
        "Support: @BDTranslate_support\n"
        "News Channel: @BD_Translate"
    )
    bot.send_message(message.chat.id, text)

def handle_donate(bot, message):
    text = (
        "☕ You can donate to support this project:\n\n"
        "TON: `UQDp1CVncTjyjtN_2Iu8rKgwRIcIp3XoJis8Jl88pLbkql4M`\n"
        "BTC: `bc1parq4cl9d2cu0k59tndvxxdjxtk74kde35hp35pevn35e588tue4sqlv4x4`\n"
        "ETH (USDT ERC20): `0x56C889b818c13955070f83D396b33A6a25eFA7CB`\n"
        "BNB (USDT BEP20): `0x56C889b818c13955070f83D396b33A6a25eFA7CB`\n"
        "SOL: `Hgo1rXUqzGpXriRsjVGWgAuv6Ag77XnfU48TdUF3aFwy`"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

def handle_about(bot, message):
    text = (
        "🌐 BD Translate Bot\n\n"
        "This bot can automatically translate messages in group chats.\n"
        "You can set two languages or enable auto-translate mode.\n"
        "Supports 15+ popular languages.\n\n"
        "To start, add the bot to your group and give admin permission."
    )
    bot.send_message(message.chat.id, text)