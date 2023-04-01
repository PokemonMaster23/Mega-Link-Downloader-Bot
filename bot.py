from pyrogram import Client, filters
from pyrogram.types import Message
import config
import logging
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

# Download command handler
@app.on_message(filters.command("download"))
async def download_handler(client: Client, message: Message):
    # Check if link is provided
    if not message.text.split(" ")[1:]:
        await message.reply_text('Please provide a valid mega.nz link')
        return
    
    link = message.text.split(" ")[1]
    logging.info(f'Downloading link: {link}')
    await message.reply_text(f'Downloading {link}...')

    # Login to Mega.nz
    mega = Mega()
    m = mega.login(config.EMAIL, config.PASSWORD)

    # Download file
    file = m.download_url(link)
    logging.info(f'Downloaded file: {file}')
    await message.reply_text(f'Downloaded file: {file}')
    
    # Upload file to Telegram
    logging.info(f'Uploading file: {file}')
    await message.reply_text(f'Uploading {file}...')
    await client.send_document(
        chat_id=message.chat.id,
        document=file,
        progress=progress_callback
    )

# Progress callback function for file upload
async def progress_callback(current, total):
    logging.info(f"Uploaded {current} out of {total} bytes ({current/total*100:.2f}%)")

# Run bot
app.run()
