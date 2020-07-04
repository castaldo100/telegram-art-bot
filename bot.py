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


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Schreib mir '/info ID' (ohne Anführungszeichen) wobei ID die Nummer eines Kunstwerkes ist und ich sende dir Informationen dazu."
        )

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

informationen = {
    '1':'ein haus',
    '2':'Drei Pfund Spaghetti Bolo auf dem Bauchnabel deiner Mudda',
    '3':'eine nackige Julia',
    '4':'ein rollmopsiger Turing, der gegrault werden will'
    }

def info(update, context):
    werk_id = ' '.join(context.args)

    if len(werk_id) < 1:
        text = 'Die ID fehlt'
    else:
        try:
            text = informationen[werk_id]
        except:
            text = str(
                'Die ID (' 
                + werk_id 
                + ') kann ich leider nicht finden.'
                + '\n'
                + "Schreib mir '/ids', um alle möglichen IDs zu erhalten"
                )   
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=text
        )

info_handler = CommandHandler('info', info)
dispatcher.add_handler(info_handler)

def ids(update, context):
    keys = []
    for key in informationen.keys():
        keys.append(key)
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text='Es gibt zu folgenden IDs Inhalte:' + str(keys)
        )

ids_handler = CommandHandler('ids', ids)
dispatcher.add_handler(ids_handler)


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



