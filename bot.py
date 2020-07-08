# Test-Bot zur Übung
# Access_Token
# 

import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

import time
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Token muss später noch als JSON geladen werden, um nicht öffentlich zu sein
Token = '1282912519:AAE2gkIO8pKAsqRKCficQRNWcW0haM_7-7k'

# Grundlegendes
bot = telegram.Bot(token=Token)
updater = Updater(token=Token, use_context=True)
dispatcher = updater.dispatcher

def info(update, context):
    werk_id = ' '.join(context.args)
    if len(werk_id) < 1:
        text = "Die Identifikationsnummer (ID) fehlt. Schreib mir z.B.: '/info 3' "
    else:
        print (type(werk_id))
        print (werk_id)
        try:
            text = context.bot_data[int(werk_id)]
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
    keys.sort()
    if len(keys) > 0:
        ids = ', '.join(keys)
    else:
        ids = "❌Leider gibt es noch keine IDs. Schreib mit '/einreichen' um der erste zu sein\n"
    update.message.reply_text(
        "Es gibt Texte über die Kunstwerke mit den folgenden IDs:\n\n" 
        + str(ids) + "\n\n"
        + "[🧐 Eine ID ist eine Nummer, die du meistens neben dem Titel des Kunstwerkes findest]")

ids_handler = CommandHandler('ids', ids)
dispatcher.add_handler(ids_handler)


def einreichen(update, context):
    if update.message.text == '/einreichen':
        update.message.reply_text("Jetzt kannst du deine eigenen Texte hinzufügen. Ein Beispiel wäre:\n\n")
        update.message.reply_text("/einreichen 2 Das blaue Pferd von Franz Mark ist mein liebstes Gemälde")
    else:
        try:
            werk_id =  int(update.message.text.split(' ')[1])
            text = update.message.text.split(' ')[2:]
            context.bot_data[werk_id] = ' '.join(text)
            update.message.reply_text(
                "Danke. 😎Dein Eintrag wurde gespeichert.🎉\n\n" 
                "Wenn du mir: \n\n/info "
                + str(werk_id) + "\n\n"
                + " schreibst, findest du deinen Eintrag.🙋🏽")
        except:
            update.message.reply_text("Es fehlt wohl die ID. 😱Schreibe mir '/einreichen', um ein Beispiel zu sehen.")


einreichen_handler = CommandHandler('einreichen', einreichen)
dispatcher.add_handler(einreichen_handler) 



def start(update, context):
    update.message.reply_text(
        "Hi! Ich bin Artsy-Bot. 🤖🖼\n"
        "Ich habe 2 Funktionen: \n "
        "1. Ich texte dir einen Gedanken über ein bestimmtes Kunstwerk.\n"
        "2. Du kannst mir DEINE Gedanken über ein bestimmtes Kunstwerk schreiben, sodass jemand anderes sie lesen kann.\n"
        "❌ Mehr kann ich nicht – und ich werde auch nicht auf deine sonstigen Nachrichten reagieren können. Sorry 😅\n\n"
    )
    time.sleep(12)
    update.message.reply_text(
        "1. Damit du weißt, welche Kunstwerke bereits einen Text haben, nutze den Button /ids\n"
        "Wenn du die ID von einem Kunstwerk gefunden hast, schreibe mir z.B.: \n\n/info 32 \n\ndann sende ich dir den Text zum Kunstwerk mit der ID 32.\n\n"
        )
    time.sleep(13)
    update.message.reply_text(
        "2. Wenn du einen Text einreichen magst, schreibe mir z.B. \n\n/einreichen 32 Ich finde das Gemälde erinnert mich an meine Heimat\n\nund schon hast du anonym einen Text zum Kunstwerk mit der ID 32 verfasst. \n\n"
        )
    time.sleep(10)
    update.message.reply_text(
        "Diesen Text lesen nun die anderen Nutzer, wenn sie mir \n\n/info 32\n\nschreiben.\n\n"
        )
    time.sleep(5)
    update.message.reply_text(
        "Eine ausführliche Erklärung und die Datenschutzrichtlinien findest du auf kulturdata.de\n\n"
        )
    button_list = [[
            telegram.InlineKeyboardButton('/info'),
            telegram.InlineKeyboardButton('/ids'),
            telegram.InlineKeyboardButton('/einreichen')
        ]]
    reply_markup = telegram.ReplyKeyboardMarkup(button_list)
    bot.send_message(chat_id=update.effective_chat.id, text="Hier findest du die Buttons 👇🏻", reply_markup=reply_markup)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)



# Geht mit unbekannten Commands um
# Muss am Ende stehen
def unknown(update, context):
    update.message.reply_text(
        "Es tut mir leid, diesen Befehl kenne ich nicht 😭\n")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

# Startet das Bot
updater.start_polling()
# Script stoppen mit ctrl + c
updater.idle() # wartet auf ctrl + c 