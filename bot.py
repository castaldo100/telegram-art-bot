# Test-Bot zur Übung
# Access_Token
# 

import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from functools import wraps
from telegram import ParseMode
from telegram.utils.helpers import mention_html

import time
import sys
import traceback
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Token muss später noch als JSON geladen werden, um nicht öffentlich zu sein
Token = '1282912519:AAE2gkIO8pKAsqRKCficQRNWcW0haM_7-7k'

# Grundlegendes
bot = telegram.Bot(token=Token)
updater = Updater(token=Token, use_context=True)
dispatcher = updater.dispatcher


# this is a general error handler function. If you need more information about specific type of update, add it to the
# payload in the respective if clause
def error(update, context):
    # add all the dev user_ids in this list. You can also add ids of channels or groups.
    devs = [1294687064] # Meine ID
    # we want to notify the user of this problem. This will always work, but not notify users if the update is an 
    # callback or inline query, or a poll update. In case you want this, keep in mind that sending the message 
    # could fail
    if update.effective_message:
        text = "Hey. I'm sorry to inform you that an error happened while I tried to handle your update. " \
               "My developer(s) will be notified."
        update.effective_message.reply_text(text)
    # This traceback is created with accessing the traceback object from the sys.exc_info, which is returned as the
    # third value of the returned tuple. Then we use the traceback.format_tb to get the traceback as a string, which
    # for a weird reason separates the line breaks in a list, but keeps the linebreaks itself. So just joining an
    # empty string works fine.
    trace = "".join(traceback.format_tb(sys.exc_info()[2]))
    # lets try to get as much information from the telegram update as possible
    payload = ""
    # normally, we always have an user. If not, its either a channel or a poll update.
    if update.effective_user:
        payload += f' with the user {mention_html(update.effective_user.id, update.effective_user.first_name)}'
    # there are more situations when you don't get a chat
    if update.effective_chat:
        payload += f' within the chat <i>{update.effective_chat.title}</i>'
        if update.effective_chat.username:
            payload += f' (@{update.effective_chat.username})'
    # but only one where you have an empty payload by now: A poll (buuuh)
    if update.poll:
        payload += f' with the poll id {update.poll.id}.'
    # lets put this in a "well" formatted text
    text = f"Hey.\n The error <code>{context.error}</code> happened{payload}. The full traceback:\n\n<code>{trace}" \
           f"</code>"
    # and send it to the dev(s)
    for dev_id in devs:
        context.bot.send_message(dev_id, text, parse_mode=ParseMode.HTML)
    # we raise the error again, so the logger module catches it. If you don't use the logger module, use it.
    raise

def info(update, context):
    werk_id = ' '.join(context.args)

    if len(werk_id) < 1:
        text = "Die Identifikationsnummer (ID) fehlt. Schreib mir z.B.: '/info 3' "
    else:
        try:
            text = context.bot_data[werk_id]
        except:
            text = str(
                "Zur ID (" + werk_id + ") kann ich leider nichts finden.🥺\n"
                "Schreibe mir '/ids', um alle IDs mit Texten zu erhalten"
                )   
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=text
        )

info_handler = CommandHandler('info', info)
dispatcher.add_handler(info_handler)

def ids(update, context):
    keys = []
    for key in context.bot_data.keys():
        keys.append(str(key))
    if len(keys) > 0:
        ids = ', '.join(keys)
    else:
        ids = "❌Leider gibt es noch keine Ids. Schreib mit '/einreichen' um der erste zu sein\n"
    update.message.reply_text(
        "Es gibt Texte über die Kunstwerke mit den folgenden IDs:\n" 
        + str(ids) + "\n\n"
        + "🧐 Eine ID ist eine Nummer, die du meistens neben dem Titel des Kunstwerkes findest")

ids_handler = CommandHandler('ids', ids)
dispatcher.add_handler(ids_handler)

def einreichen(update, context):
    if update.message.text == '/einreichen':
        update.message.reply_text("Hier kannst du deine eigenen Texte hinzufügen")
        update.message.reply_text("Beispiel: '/einreichen 2 Das blaue Pferd von Franz Mark ist mein liebstes Gemälde")
    else:
        try:
            werk_id =  int(update.message.text.split(' ')[1])
            text = update.message.text.split(' ')[2:]
            context.bot_data[werk_id] = ' '.join(text)
            update.message.reply_text("Danke. 😎Dein Eintrag wurde gespeichert. 🎉")
        except:
            update.message.reply_text("Es fehlt wohl die ID. 😱Schreibe mir '/einreichen', um ein Beispiel zu sehen.")


einreichen_handler = CommandHandler('einreichen', einreichen)
dispatcher.add_handler(einreichen_handler) 



def start(update, context):
    update.message.reply_text(
        "Hi! Ich bin Artsy-Bot. 🤖🖼\n"
        "Ich habe 2 Funktionen: \n "
        "1. Ich texte dir einen Gedanken über ein bestimmtes Kunstwerk\n"
        "2. Du kannst mir DEINE Gedanken über ein bestimmtes Kunstwerk schreiben, sodass jemand anderes sie lesen kann\n"
        "❌ Mehr kann ich nicht – und ich werde auch nicht auf deine sonstigen Nachrichten reagieren können. Sorry 😅\n\n"
    )
    time.sleep(5)
    update.message.reply_text(
        "Damit du weißt, welche Kunstwerke bereits einen Text haben, nutze den Button '/ids'\n"
        "Wenn du die ID von einem Kunstwerk gefunden hast, schreibe mir z.B. '/info 32', dann sende ich dir den Text zum Kunstwerk mit der ID 32\n"
        "Wenn du einen Text einreichen magst, schreibe mir z.B. '/einreichen 32 Ich finde das Gemälde erinnert mich an meine Heimat' und schon hast du anonym einen Text zum Kunstwerk mit der ID 32 verfasst. \n"
        "Diesen Text lesen nun die anderen Nutzer, wenn sie mir '/info 32' schreiben.\n"
        "Eine ausführliche Erklärung und die Datenschutzrichtlinien findest du auf kulturdata.de"
        )
    button_list = [[
            telegram.InlineKeyboardButton('/info'),
            telegram.InlineKeyboardButton('/ids'),
            telegram.InlineKeyboardButton('/einreichen')
        ]]
    reply_markup = telegram.ReplyKeyboardMarkup(button_list)
    bot.send_message(chat_id=update.effective_chat.id, text="👇🏻 hier findest du die Buttons", reply_markup=reply_markup)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)



# Geht mit unbekannten Commands um
# Muss am Ende stehen
def unknown(update, context):
    update.message.reply_text("Es tut mir leid, diesen Befehl kenne ich nicht 😭")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

# Startet das Bot
updater.start_polling()
# Script stoppen mit ctrl + c
updater.idle() # wartet auf ctrl + c 