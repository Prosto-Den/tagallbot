import os


class FileManipulator:
    """
    Класс для выполнения операция над файлами
    """
    @classmethod
    def create_folder(cls, path: str) -> None:
        """
        Создаёт папку по указанному пути, если она не существует
        :param path: Путь к папке
        """
        if not os.path.exists(path):
            os.mkdir(path)

