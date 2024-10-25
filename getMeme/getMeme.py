import os
from settings import PATH_TO_MEMES
from random import choice


def get_random_meme() -> str:
    return PATH_TO_MEMES + '/' + choice(os.listdir(PATH_TO_MEMES))