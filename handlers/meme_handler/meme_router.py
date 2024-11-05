from aiogram import Router
from .add_meme import add_meme_router

meme_router = Router()
meme_router.include_router(add_meme_router)
