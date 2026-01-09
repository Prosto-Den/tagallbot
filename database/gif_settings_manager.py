from enum import StrEnum
from database.db_manager import DBManager
from models.database_models import GifSettingsModel


class GIFSettingsSQL(StrEnum):
    """
    Запросы для SQL
    """
    # создать таблицу, если её ещё нет
    CREATE_GIF_SETTINGS_TABLE = ("CREATE TABLE IF NOT EXISTS gif_settings("
                                 "user_id INTEGER PRIMARY KEY,"
                                 "height INTEGER NOT NULL,"
                                 "width INTEGER NOT NULL,"
                                 "speed INTEGER NOT NULL"
                                 ");")
    # добавить новую запись в таблицу
    ADD_SETTINGS = "INSERT INTO gif_settings VALUES (?, ?, ?, ?);"
    # получить настройки по ID пользователя
    GET_SETTINGS = "SELECT * FROM gif_settings WHERE user_id=?;"
    # обновить настройки у пользователя
    UPDATE_SETTINGS = 'UPDATE gif_settings SET height = :2, width = :3, speed = :4 WHERE user_id = :1;'


class GifSettingManager:
    @classmethod
    async def get_or_create_settings(cls, user_id: int) -> GifSettingsModel:
        model = await DBManager.execute_one(GIFSettingsSQL.GET_SETTINGS, GifSettingsModel, user_id)
        if model is None:
            default = GifSettingsModel(user_id)
            await cls.add_settings(default)
            return default
        return model

    @classmethod
    async def add_settings(cls, model: GifSettingsModel) -> None:
        await DBManager.execute(GIFSettingsSQL.ADD_SETTINGS, model.as_tuple())

    @classmethod
    async def update_settings(cls, model: GifSettingsModel) -> None:
        await DBManager.execute(GIFSettingsSQL.UPDATE_SETTINGS, model.as_tuple())
