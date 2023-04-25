from pyrogram import Client, filters, types
from pyrogram.types import Message
import config
import logging
import time
import threading
import asyncio
import os
from mega import Mega

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initialize Pyrogram client
app = Client(
    "MegaLinkDownloaderBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

# Start command handler
@app.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    await message.reply_text('Hello! This bot can download files from mega.nz')


# List to store download tasks
download_tasks = []

# Callback function for progress of document upload
async def progress_callback(current: int, total: int, message: Message):
    progress = current * 100 / total
    logging.info(f"Uploading document: {message.document.file_name} - {progress:.2f}%")

# Download command handler
@app.on_message(filters.command("download"))
async def download_handler(client: Client, message: Message):
    # Check if link is provided
    if not message.text.split(" ")[1:]:
        await message.reply_text('Please provide a valid mega.nz link')
        return None
    
    link = message.text.split(" ")[1]
    logging.info(f'Downloading link: {link}')
    await message.reply_text(f'Downloading {link}...')


    # Create a new thread for downloading
    download_thread = threading.Thread(target=download_task, args=(link, client,message))
    download_thread.start()

    # Add task to list
    download_tasks.append(link)
    logging.info(f'Download tasks: {download_tasks}')

    print(download_tasks)


# Download
def download_task(link, client,message):
    # Initialize mega.py
    mega = Mega()
    mega.login(config.EMAIL, config.PASSWORD)

    # Download file
    md = mega.download_url(link)
    
     # Upload file to Telegram
    logging.info(f'Uploading file: {md}')
    message.reply_text(f'Uploading {md}... - @{message.chat.username}')
    time.sleep(5)
    # Send file to User
    client.send_document(
        chat_id=message.chat.id,
        document=md
    )
    

    # Remove file from local storage
    os.remove(md)


# List command handler
@app.on_message(filters.command("list"))
async def list_handler(client: Client, message: Message):
    # Check if there are any files in the download list
    if not download_tasks:
        await message.reply_text('No files in the download list.')
        return None
    
    # Send the list of files to the user
    file_list = '\n'.join(download_tasks)
    await message.reply_text(f'Download list:\n{file_list}')



# Run bot
app.run()
