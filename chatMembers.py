from pyrogram import Client
from settings import API_HASH, API_ID



async def get_chat_members(chat_id: int) -> list:
    async with Client('my_account', API_ID, API_HASH) as app:
        for member in await app.get_chat_members(chat_id):
            print(member)
