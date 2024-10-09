from pyrogram import Client
from settings.settings import API_HASH, API_ID
from pyrogram.types import ChatMember


async def get_chat_members(chat_id: int) -> list:
    result = list()

    async with Client('my_account', API_ID, API_HASH) as app:
        member: ChatMember
        async for member in app.get_chat_members(chat_id):
            if not member.user.is_bot:
                username: str = '@' + member.user.username + '\n'
                result.append(username)

    return result
