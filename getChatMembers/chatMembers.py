from pyrogram import Client, utils
from settings import API_HASH, API_ID
from pyrogram.types import ChatMember




async def get_chat_members(chat_id: int) -> list:
    def get_peer_type_new(peer_id: int) -> str:
        peer_id_str = str(peer_id)
        if not peer_id_str.startswith("-"):
            return "user"
        elif peer_id_str.startswith("-100"):
            return "channel"
        else:
            return "chat"

    utils.get_peer_type = get_peer_type_new

    result = list()

    # Будут создаваться сессии с id чата в названии. Да, будет много файлов, но так, вроде бы, бот должен
    # будет работать во всех чатах, где он есть. Однако файл .session не будет добавляться в файл .gitignore.
    # Не безопасно, надо будет посмотреть пути решения
    app: Client
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
