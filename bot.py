pyrogram
def start_handler(event):
    client.send_message(event.chat_id, 'Hi! I can download files from Mega.nz links. Just send me the link and I will download the file and send it to you!')

# Handler function for files sent to the bot
def download_handler(event):
    # Check if the message has a mega.nz link
    message_text = event.message.message
    mega_match = mega_link_pattern.search(message_text)
    if mega_match is None:
        return

    # Get the Mega.nz link and key from the match object
    file_id = mega_match.group(1) or mega_match.group(3)
    file_key = mega_match.group(2)

    # Download the file from Mega.nz
    client.send_message(event.chat_id, 'Downloading file...')
    mega_file = mega.get_public_link(file_id, file_key)
    file_name = mega_file['name']
    file_data = requests.get(mega_file['url']).content

    # Save the file locally and send it to the user
    with open(file_name, 'wb') as f:
        f.write(file_data)
    attributes = [DocumentAttributeFilename(file_name)]
    try:
        client.send_file(event.chat_id, file_name, attributes=attributes)
    except PeerIdInvalidError:
        client.send_message(event.chat_id, 'Error sending file: Invalid chat ID')

# Start the bot
client.connect()
client.add_event_handler(start_handler, events.NewMessage(pattern='/start'))
client.add_event_handler(download_handler, events.NewMessage(func=lambda event: True))
client.start()
client.run_until_disconnected()
