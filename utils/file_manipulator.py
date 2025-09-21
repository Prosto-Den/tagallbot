import os


class FileManipulator:
    @classmethod
    def create_folder(cls, path: str) -> None:
        if not os.path.exists(path):
            os.mkdir(path)
