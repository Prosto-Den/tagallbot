import sqlite3 as sq
from typing import Self
from .model import Meme
from random import randint

class Connection:
    __instance: Self = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self):
        self.__connection = sq.connect('memes.db')

        self.__connection.execute('create table if not exists memes('
                                  'id text primary key,'
                                  'name text,'
                                  'tags text)')
        
        self.__connection.execute('create table if not exists arxive('
                                  'id integer primary key AUTOINCREMENT,'
                                  'chat_id integer,'
                                  'message_id integer,'
                                  'photo_id text)')

    def __del__(self):
        self.__connection.close()
        Connection.__instance = None

    def add_meme(self, meme: Meme) -> None:
        self.__connection.execute('INSERT INTO memes(id, name, tags) VALUES (?,?,?)',
                                  (meme.id, meme.name.lower(), meme.tags))
        self.__connection.commit()

    # я пока не знаю, надо ли это, пока закомментил
    # def get_meme(self, id: str) -> Meme | None:
    #     cursor = self.__connection.cursor()
    #     cursor.execute('SELECT * FROM memes WHERE id=?', (id,))
    #
    #     if not cursor.fetchone():
    #         return None
    #
    #     return Meme(*cursor.fetchone())

    def get_meme_by_name(self, name: str) -> Meme | None:
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM memes WHERE name=?', (name,))

        if (data := cursor.fetchone()) is None:
            return None

        return Meme(*data)

    def get_all_memes(self) -> list[Meme]:
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM memes')
        return [Meme(*row) for row in cursor.fetchall()]

    def is_photo_in_db(self, photo_id: str) -> bool:
        cursor = self.__connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM memes WHERE id=?', (photo_id,))
        return cursor.fetchone()[0] > 0

    def get_arxive_chats(self) -> list[int]:
        cursor = self.__connection.cursor()
        cursor.execute('SELECT DISTINCT chat_id FROM arxive')
        return [row[0] for row in cursor.fetchall()]

    def add_to_arxive(self, chat_id: int, message_id: int, photo_id: int) -> None:
        self.__connection.execute('INSERT INTO arxive(chat_id, message_id, photo_id) VALUES (?, ?, ?)',
                      (chat_id, message_id, photo_id))
        self.__connection.commit()

    def get_random_meme(self) -> tuple[int, int, str]:
        cursor = self.__connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM arxive")
        count = cursor.fetchone()[0]

        if count == 0:
            return None, None, None

        random_index = randint(0, count - 1)
        cursor.execute(f"SELECT chat_id, message_id, photo_id FROM arxive LIMIT 1 OFFSET {random_index}")
        return cursor.fetchone()

    def delete_from_arxive(self, chat_id: int, message_id: int) -> None:
        cursor = self.__connection.cursor()
        
        cursor.execute("DELETE FROM arxive WHERE chat_id = ? AND memessage_id = ?", (chat_id, message_id))
        self.__connection.commit()