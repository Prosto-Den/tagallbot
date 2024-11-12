from aiogram import Bot, Dispatcher
from settings import TOKEN
from database import Connection
from aiogram.types import Message

# i suggest custom class is a good way to structure and incapsulate program logic
class ProstoBot(Bot):
    def __init__(self, token: str):
        super().__init__(token=token)
        self.__conn: Connection = Connection() # anyway this is a singleton so no difference whether it is created inplace or passed to constructor
        self.__archive_chats: list[int] = conn.get_arxive_chats()

    @property
    def arxive_chats(self) -> list[int]:
        return self.__archive_chats

    def push_archive(self, message: Message) -> None:
        self.__archive_chats.append(message.chat.id)
        self.__conn.add_to_arxive(message.chat.id, message.message_id, message.photo[-1].file_id)

    def add_meme(self, meme: Message) -> None:
        self.__conn.add_to_arxive(message.chat.id, message.message_id, message.photo[-1].file_id)

    # async def get_random_meme(self) -> MessageId:
    #     chat_id, message_id, photo_id = self.__conn.get_random_meme()
    #     try:
    #         message = await self.copy_message(chat_id, message_id)
    #         return message
    #     except Exception as e:
    #         self.__conn.delete_from_arxive(chat_id, message_id)
    #         return None

conn = Connection()
bot = ProstoBot(TOKEN)
dp = Dispatcher()
