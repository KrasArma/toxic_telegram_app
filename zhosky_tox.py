import json
import re
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji

with open('credentials.json', 'r') as f:
    credentials = json.load(f)

api_id = credentials['api_id']
api_hash = credentials['api_hash']
phone_number = credentials['phone_number']


client = TelegramClient('zhosky_user_session', api_id, api_hash)


chat_ids = [
    1488,
    228
]


usernames = [
    '@tyota',
    '@dyadya'
]


keywords = ['обед', 'курить', 'смочить', 'смокиш', 'парить', "попарить", "перекур", "перекурить"]

async def main():
    await client.start(phone_number)
    
    if not await client.is_user_authorized():
        await client.sign_in(phone_number)


    user_ids = []
    for username in usernames:
        try:
            user = await client.get_entity(username)
            user_ids.append(user.id)
        except Exception as e:
            print(f"err usr {username}: {e}")

    print(f"id: {user_ids}")

    @client.on(events.NewMessage)
    async def handler(event):
        peer_id = event.message.peer_id

        chat_id = None
        if isinstance(peer_id, PeerUser):
            chat_id = peer_id.user_id
        elif isinstance(peer_id, PeerChat):
            chat_id = peer_id.chat_id
        elif isinstance(peer_id, PeerChannel):
            chat_id = peer_id.channel_id
        
        #print(event.message.peer_id, event.message.message.lower())
        if chat_id not in chat_ids:
            return
        
        sender = await event.get_sender()
        
        if sender.id not in user_ids:
            return
        
        # if sender.id == (await client.get_me()).id:
        #     return

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

    print("Zhosky")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())