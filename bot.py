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
    if not context.chat_data[update.effective_chat.id]:
        update.message.reply_text(
            "You haven't yet told me which museum you are visiting.\n\n"  
            "Please start by sending me \n/museum\n to see which museum is already part of our community."
    else:
        museum = context.chat_data[update.effective_chat.id]
        pass
        
    werk_id = ' '.join(context.args)
    if len(werk_id) < 1:
        text = "The identification number is missing. Write i.e. /info 3"
    else:
        try:
            text = context.bot_data[(museum, werk_id)]
        except:
            text = str(
                "Unfortunately, there is no record for ID " + werk_id + " 🥺\n"
                "Write /ids to see all available IDs"
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
        ids = "❌Sorry, I don't know any artworks yet. Write'/submit' and be the first collaborator!🥰\n"
    update.message.reply_text(
        "I know descriptions for the following museums and IDs:\n\n" 
        + str(ids) + "\n\n"
        + "[🧐 An ID is a so called 'Identification Number' that you will find next to the artwork to use a audio guide.]")

ids_handler = CommandHandler('ids', ids)
dispatcher.add_handler(ids_handler)

def museum(update, context):
    museum = ' '.join(context.args) 
    chat_id=update.effective_chat.id
    context.chat_data[chat_id] = museum
    print (context.chat_data)
    context.bot.send_message(
        chat_id=chat_id, 
        text="Thanks📍. Now I know which artworks to look for. If you want to change the museum, just repeat this process."
        )

museum_handler = CommandHandler('museum', museum)
dispatcher.add_handler(museum_handler) 


def submit(update, context):
    if update.message.text == '/submit':
        update.message.reply_text("Now you can submit your own description. For example:\n\n")
        update.message.reply_text("/submit 2 'Blue Horses' by Franz Marc is my favorite painting. It's so 'neighT'")
    else:
        try:
            museum = context.chat_data[update.effective_chat.id]
            werk_id =  int(update.message.text.split(' ')[1])
            text = update.message.text.split(' ')[2:]
            context.bot_data[(museum, werk_id)] = ' '.join(text)
            update.message.reply_text(
                "Thanks! – also on behalf of the whole community. 😎Your description has been saved.🎉\n\n" 
                "Write: \n\n/info "
                + str(werk_id) + "\n\n"
                + " to find your submission. 🙋🏽")
        except:
            update.message.reply_text("The ID seems to be missing. 😱Write /submit to find an example.")


submit_handler = CommandHandler('submit', submit)
dispatcher.add_handler(submit_handler) 



def start(update, context):
    update.message.reply_text(
        "Hi, I'm Artsy-Bot! 🤖🖼\n"
        "I have 2 functions: \n "
        "1. I can tell you something about a specific artwork\n"
        "2. YOU can tell me something about an artwork so I can share your text with other users\n"
        "❌ That's all I can do. And I'm like your sh*tty ex boyfriend and will ghost you, if you ask me anything else. 👻😅\n\n"
    )
    time.sleep(12)
    update.message.reply_text(
        "1. Use the button /ids to find out which artworks I already know something about.\n"
        "When you have found the ID of an artwork you're interested in, just write i.e.:\n\n/info 32 \n\nthen I will send you the corresponding text to the artwork with the ID 32\n\n"
        )
    time.sleep(13)
    update.message.reply_text(
        "2. If you want to submit a text, write\n\n/submit 32 The painting reminds me of home.\n\nThat's all you have to do to anonymously submit your description for artwork 32.\n\n"
        )
    time.sleep(10)
    update.message.reply_text(
        "Other people can now access this description when the write\n\n/info 32\n\n"
        )
    time.sleep(5)
    update.message.reply_text(
        "A more detailed explanation and the data privacy statement at kulturdata.de\n\n"
        )
    button_list = [[
            telegram.InlineKeyboardButton('/info'),
            telegram.InlineKeyboardButton('/ids'),
            telegram.InlineKeyboardButton('/submit')
        ]]
    reply_markup = telegram.ReplyKeyboardMarkup(button_list)
    bot.send_message(chat_id=update.effective_chat.id, text="Find the buttons below 👇🏻", reply_markup=reply_markup)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)



# Geht mit unbekannten Commands um
# Muss am Ende stehen
def unknown(update, context):
    update.message.reply_text(
        "I'm deeply sorry. I don't know this command. Maybe a typo? 😭\n")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

# Startet das Bot
updater.start_polling()
# Script stoppen mit ctrl + c
updater.idle() # wartet auf ctrl + c 