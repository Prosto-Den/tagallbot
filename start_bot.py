from bot import dp, bot
from handlers import messages_router
from aiogram.methods import DeleteWebhook
import asyncio


async def main():
    await bot(DeleteWebhook(drop_pending_updates = True))
    dp.include_router(messages_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
