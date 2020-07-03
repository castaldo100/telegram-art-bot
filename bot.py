# Test-Bot zur Übung
# Access_Token
# 

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from translate import Translator
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Token muss später noch als JSON geladen werden, um nicht öffentlich zu sein
Token = '1282912519:AAE2gkIO8pKAsqRKCficQRNWcW0haM_7-7k'

# Grundlegendes
bot = telegram.Bot(token=Token)
updater = Updater(token=Token, use_context=True)
dispatcher = updater.dispatcher


def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Stunden bis Wochenende',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)

inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)

# Geht mit unbekannten Commands um
# Muss am Ende stehen
def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Es tut mir leid, diesen Befehl gibt es nicht."
        )

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

# Startet das Bot
updater.start_polling()
# Script stoppen mit ctrl + c
updater.idle() # wartet auf ctrl + c 



