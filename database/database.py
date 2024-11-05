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

    def get_meme(self, id: str) -> Meme:
        cursor = self.__connection.cursor()
        cursor.execute('SELECT * FROM memes WHERE id=?', (id,))
        return Meme(*cursor.fetchone())


