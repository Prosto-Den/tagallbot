import os
from settings import PATH_TO_MEMES
from random import choice

"""Пока что в тестовом режиме, сюда не смотрим"""


def get_random_meme() -> str:
    return PATH_TO_MEMES + '/' + choice(os.listdir(PATH_TO_MEMES))