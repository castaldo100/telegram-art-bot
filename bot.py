# Test-Bot zur Übung
# Access_Token
# 

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

Token = '1282912519:AAE2gkIO8pKAsqRKCficQRNWcW0haM_7-7k'
# Token muss später noch als JSON geladen werden, um nicht öffentlich zu sein


bot = telegram.Bot(token=Token)
updater = Updater(token=Token, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, 
    text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Startet das Bot
updater.start_polling()

