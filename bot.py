import os
import mega
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import TOKEN, MEGA_EMAIL, MEGA_PASSWORD

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! Send me a Mega.nz link and I will download it for you.')

def download_mega(update, context):
    """Download file from Mega.nz link."""
    url = update.message.text
    try:
        m = mega.login(MEGA_EMAIL, MEGA_PASSWORD)
        file = m.find(url)
        if file:
            file.download(os.getcwd())
            update.message.reply_text('File downloaded successfully!')
        else:
            update.message.reply_text('File not found. Please check your Mega.nz link.')
    except Exception as e:
        update.message.reply_text('Error: {}'.format(str(e)))

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_mega))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
