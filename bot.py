# Test-Bot zur Übung
# Access_Token
# 

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
from functools import wraps
from telegram import ParseMode
from telegram.utils.helpers import mention_html

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

def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=telegram.ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func

@send_typing_action
def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Schreib mir '/info ID' (ohne Anführungszeichen) wobei ID die Nummer eines Kunstwerkes ist und ich sende dir Informationen dazu."
        )

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

informationen = {
    '1':'ein haus',
    '2':'ein blaues Haus',
    '3':'ein Portrait',
    '4':'ein Kater, der grault werden will',
    '5': 'Neues Item',
    '7751':'Kein anderes Bild Spitzwegs erfreut sich heute so großer Popularität wie der "arme Poet". Das Klischee des sich nur auf das Geistige konzentrierenden Dichters, den materielle Äußerlichkeiten nicht interessieren, hat Spitzweg hier prototypisch ins Bild gesetzt: In einem schäbigen Dachzimmer auf einer Matratze liegend, gegen die Kälte mit einer Decke, einer abgewetzten Jacke und einer Schlafhaube ausgerüstet und mit einem Schirm gegen eindringendes Regenwasser geschützt, scheint der Dichter sich unbeirrt von den widrigen äußeren Bedingungen ganz der Ausarbeitung eines Gedichtes zu widmen. Als das Bild 1839 im Münchner Kunstverein der Öffentlichkeit vorgestellt wurde, stieß es allerdings mit seiner ironisierenden Darstellung des verarmten Dichters auf Kritik. Man verstand das Bild als Angriff auf die Idealität der Dichtkunst und zugleich als Angriff auf die idealisierende Kunst schlechthin, wie sie vor allem durch die akademische Historienmalerei vertreten wurde. Auch werden die oft elenden Umstände deutlich, unter denen eine Vielzahl verarmter Künstler zu leiden hatte, und wird die von Zeitgenossen diskutierte Frage nach dem Sinn und Zweck einer überquellenden, aber oft nur mittelmäßigen Kunstproduktion gestellt: die Werke des Dichters liegen vor dem Ofen als Heizmaterial bereit.'
    }

@send_typing_action
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

@send_typing_action
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