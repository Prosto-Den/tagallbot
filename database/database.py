import sqlite3 as sq
from typing import Self
from .model import Meme


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

    def __del__(self):
        self.__connection.close()
        Connection.__instance = None

    def add_meme(self, meme: Meme) -> None:
        self.__connection.execute('INSERT INTO memes(id, name, tags) VALUES (?,?,?)',
                                  (meme.id, meme.name.lower(), meme.tags))
        self.__connection.commit()

    def get_meme(self, id: str) -> Meme | None:
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM memes WHERE id=?', (id,))

        if not cursor.fetchone():
            return

        return Meme(*cursor.fetchone())

    def get_all_memes(self) -> list[Meme]:
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM memes')
        return [Meme(*row) for row in cursor.fetchall()]

    def is_photo_in_db(self, photo_id: str) -> bool:
        cursor = self.__connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM memes WHERE id=?', (photo_id,))
        return cursor.fetchone()[0] > 0