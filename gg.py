
import json
import re
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji


with open('credentials.json', 'r') as f:
    credentials = json.load(f)

api_id = credentials['api_id']
api_hash = credentials['api_hash']
phone_number = credentials['phone_number']
chat_ids = credentials['chat_ids']

keywords = ['обед', 'курить', 'смочить', 'смокиш', 'парить']

client = TelegramClient('user', api_id, api_hash)

async def main():
    await client.start(phone_number)
    

    @client.on(events.NewMessage)
    async def handler(event):

        if event.message.peer_id.user_id not in chat_ids and event.message.peer_id.channel_id not in chat_ids:
            return

        sender = await event.get_sender()
        if sender.id == (await client.get_me()).id:
            return

        message_text = event.message.message.lower()


        contains_keyword = any(re.search(rf'\b{keyword}\b', message_text, re.IGNORECASE) for keyword in keywords)


        if not contains_keyword:
            await client(SendReactionRequest(
                peer=event.message.peer_id,
                msg_id=event.message.id,
                reaction=[ReactionEmoji(emoticon="👎")] 
            ))

        if contains_keyword:
            await client.send_message('me', event.message.message)

    print("toxic start!")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())