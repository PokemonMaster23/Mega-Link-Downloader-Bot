python
import os
import re
import requests
from mega import Mega
from telethon import TelegramClient, events
from telethon.errors.rpcerrorlist import PeerIdInvalidError
from telethon.tl.types import DocumentAttributeFilename

# Import configuration variables from config.py
from config import API_ID, API_HASH, BOT_TOKEN

# Initialize the Telegram client and the Mega client
client = TelegramClient('mega_downloader', API_ID, API_HASH)
mega = Mega()

# Pattern for detecting Mega.nz links in messages
mega_link_pattern = re.compile(r'https?://mega.nz/(\w+)#(\w+)|https?://mega.nz/(\w+)')

# Handler function for the '/start' command
@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await event.reply('Hi! I can download files from Mega.nz links. Just send me the link and I will download the file and send it to you!')

# Handler function for files sent to the bot
@client.on(events.NewMessage(func=lambda event: True))
async def download_handler(event):
    # Check if the message has a mega.nz link
    message_text = event.message.message
    mega_match = mega_link_pattern.search(message_text)
    if mega_match is None:
        return

    # Get the Mega.nz link and key from the match object
    file_id = mega_match.group(1) or mega_match.group(3)
    file_key = mega_match.group(2)

    # Download the file from Mega.nz
    await event.reply('Downloading file...')
    mega_file = mega.get_public_link(file_id, file_key)
    file_name = mega_file['name']
    file_data = requests.get(mega_file['url']).content

    # Save the file locally and send it to the user
    with open(file_name, 'wb') as f:
        f.write(file_data)
    attributes = [DocumentAttributeFilename(file_name)]
    try:
        await client.send_file(event.chat_id, file_name, attributes=attributes)
    except PeerIdInvalidError:
        await event.reply('Error sending file: Invalid chat ID')

# Start the bot
client.start(bot_token=BOT_TOKEN)
client.run_until_disconnected()
```
