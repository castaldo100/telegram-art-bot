"""
User generated MUSEUM GUIDE on the messenger app 'telegram'. 
Works at every museum which shows an identification number next to an exhibit.
Telegram Bot made by © Holger Kurtz | KulturData.de

[Learn how to do your own bot at https://github.com/python-telegram-bot/python-telegram-bot/wiki ]
"""

import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

import json
import time
import logging

# Logging stuff
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
    )

# Get Telegram Token from file: creds.json
telegram_credential_path = 'telegram_creds.json'
with open(telegram_credential_path, "r") as json_file:
    telegram_creds = json.load(json_file)
TOKEN = telegram_creds["Token"]

# Basics to start a Bot
bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

"""
Information is stored like this:

bot_data = {
    ('museum','id') : 'text'
}

chat_data = {
    'user_id' : 'museum' # so the user can change to a museum without changing the bot_data Database
}

"""

# /info
def info(update, context):
    werk_id = ' '.join(context.args) # Takes the word after /info
    
    if not context.chat_data:
        text = str(
            "You haven't yet told me which museum you are visiting.\n\n"
            + "Please start by sending me \n/ids\n"
            + "to see which museum is already part of our community."
        )
    else:
        museum = context.chat_data[update.effective_chat.id]
        if len(werk_id) < 1:
            text = "The identification number is missing. Write i.e. /info 3"
        else:
            try:
                text = context.bot_data[(museum, werk_id)]
            except:
                text = str(
                    "Unfortunately, there is no record for ID " 
                    + werk_id + " 🥺\n"
                    "Write /ids to see all available IDs"
                    )          
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=text
        )
# Adds the function to the bot
info_handler = CommandHandler('info', info)
dispatcher.add_handler(info_handler)

# /ids
def ids(update, context):
    try: # Check if user already checked into a museum
        museum = context.chat_data[update.effective_chat.id]
    except:
        museum = "" # No check-in yet
    
    keys = []
    for key in context.bot_data.keys(): # Tuple as Key for dict
        if key[0] == museum: # Filters the ids (type: tuple) for the museum
            keys.append(key[1])
        else:
            pass
    keys.sort()

    if len(keys) > 0:
        ids = ', '.join(keys)
    else:
        ids = "❌Sorry, I don't know any exhibits or museums yet. 1. Write /museum YOUR MUSEUM to check into your museum. 2. Write'/submit' and be the first collaborator in this museum!🥰\n"
    update.message.reply_text(
        "Name of the Museum:\n"
        + museum
        + "\n\nI know descriptions for the following IDs:\n\n" 
        + str(ids) + "\n\n"
        + "[🧐 An ID is a so called 'Identification Number' that you will find next to the exhibit to use an audio guide. Some exhibits might not have an ID 🥺]")

ids_handler = CommandHandler('ids', ids)
dispatcher.add_handler(ids_handler)

# /museum
def museum(update, context):
    museum = ' '.join(context.args).lower() # MET New York, met New York --> met new york
    if len(museum) < 1: # is user only writes /museum
        museum_keys = []
        for key in context.bot_data.keys():
            museum_keys.append(str(key[0])) 
        
        museum_keys = set(sorted(museum_keys)) # Only unique museums should be displayed
        
        if len(museum_keys) > 0:
            ids = ', '.join(museum_keys)
        else:
            ids = "❌Sorry, I don't know any museum yet. 1. Write /museum YOUR MUSEUM to check into your museum. 2. Write'/submit' and be the first collaborator in this museum!🥰\n"
        
        update.message.reply_text(
            "I know descriptions for the following museums:\n\n" 
            + str(ids) + "\n\n"
            + "☞ When you check in to your museum via /museum YOUR MUSEUM, make sure to type the name of the museum exactly like in this list.")
    else: # if user writes i.e. /museum met new york
        chat_id=update.effective_chat.id
        context.chat_data[chat_id] = museum
        context.bot.send_message(
            chat_id=chat_id, 
            text="Thanks📍 Welcome to: "
            + str(museum)
            + " Now I know which exhibits to look for. " 
            + "If you want to change the museum, just repeat this process."
            )

museum_handler = CommandHandler('museum', museum)
dispatcher.add_handler(museum_handler) 

# /submit 
def submit(update, context):
    if not context.chat_data: # check if user already checked into a museum
        update.message.reply_text(
            "Before you can submit a text, please tell me which museum you're visiting. " 
            + "Please send me:\n\n/museum\n\nto get started.😎"
            )
    else:
        if update.message.text == '/submit':
            update.message.reply_text("Now you can submit your own description. For example:\n\n")
            update.message.reply_text("/submit 2 'Blue Horses 🐴' by Franz Marc is my favorite painting. It's so 'neighT'") # get it? 😅
        else:
            try:
                museum = context.chat_data[update.effective_chat.id]
                werk_id =  update.message.text.split(' ')[1]
                text = update.message.text.split(' ')[2:]
                context.bot_data[(museum, werk_id)] = ' '.join(text)
                update.message.reply_text(
                    "Thanks! – also on behalf of the whole community. 😎Your description has been saved.🎉\n\n" 
                    "Write: \n\n/info "
                    + str(werk_id) + "\n\n"
                    + " to find your submission. 🙋🏽")
            except:
                update.message.reply_text("There was an error – sorry. 😱Write /submit to find an example.")


submit_handler = CommandHandler('submit', submit)
dispatcher.add_handler(submit_handler) 


# /start Explanation of the bot
def start(update, context):
    update.message.reply_text(
        "Hi, I'm Artsy-Bot! 🤖🖼\n"
        "I have 2 functions: \n"
        "1. I can tell you something about a specific exhibit\n"
        "2. YOU can tell me something about an exhibit so I can share your text with other users\n"
        "❌ That's all I can do. And I'm like your sh*tty ex boyfriend and will ghost you, if you ask me anything else. 👻😅\n\n"
    )
    time.sleep(12)
    update.message.reply_text(
        "1. Use the button /museum to find out which museums I already know something about.\n"
        "When you have found the museum you're visiting, just write i.e.:\n\n/museum met new york \n\nthen we're ready to talk art.\n\n"
        )
    time.sleep(13)
    update.message.reply_text(
        "2. Use the button /ids to find out which exhibit I already know something about.\n"
        "When you have found the ID of an exhibit you're interested in, just write i.e.:\n\n/info 32 \n\nthen I will send you the corresponding text to the exhibit with the ID 32\n\n"
        )
    time.sleep(13)
    update.message.reply_text(
        "3. If you want to submit a text, write\n\n/submit 32 The painting reminds me of home.\n\n✅ That's all you have to do to anonymously submit your thoughts on exhibit 32.\n\n"
        )
    time.sleep(10)
    update.message.reply_text(
        "4. Other people can now access this description when the write\n\n/info 32\n\n"
        )
    time.sleep(5)
    update.message.reply_text(
        "A more detailed explanation and the data privacy statement at kulturdata.de\n\n"
        )
    button_list = [[
            telegram.InlineKeyboardButton('/museum'),
            telegram.InlineKeyboardButton('/ids'),
            telegram.InlineKeyboardButton('/submit'),
            telegram.InlineKeyboardButton('/info')
        ]]
    reply_markup = telegram.ReplyKeyboardMarkup(button_list)
    bot.send_message(chat_id=update.effective_chat.id, text="Find the buttons below 👇🏻", reply_markup=reply_markup)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Handle the unknown 👀
def unknown(update, context):
    update.message.reply_text(
        "I'm deeply sorry. I don't know this command. Maybe a typo? 😭\n")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

# Starting the bot
# For stopping the bot press: ctrl + c 
updater.start_polling()
updater.idle() 