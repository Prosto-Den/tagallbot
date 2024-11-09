from aiogram import Router
from .add_meme import add_meme_router
from .get_meme import get_meme_router
from .add_arxive import add_archive_router

meme_router = Router()
meme_router.include_routers(add_meme_router, get_meme_router, add_archive_router)
