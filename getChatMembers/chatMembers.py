from pyrogram import Client
from settings import API_HASH, API_ID
from pyrogram.types import ChatMember


async def get_chat_members(chat_id: int) -> list:
    result = list()

    # Будут создаваться сессии с id чата в названии. Да, будет много файлов, но так, вроде бы, бот должен
    # будет работать во всех чатах, где он есть. Однако файл .session не будет добавляться в файл .gitignore.
    # Не безопасно, надо будет посмотреть пути решения
    async with Client(str(chat_id), API_ID, API_HASH) as app:
        member: ChatMember
        async for member in app.get_chat_members(chat_id):
            if not member.user.is_bot:
                if member.user.username:
                    username: str = '@' + member.user.username + '\n'
                    result.append(username)
                else:
                    # Нужно протестировать, что тег по id работает
                    username: str = '@' + str(member.user.id) + '\n'
                    result.append(username)

    return result
