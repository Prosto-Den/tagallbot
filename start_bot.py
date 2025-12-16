from bot import dp, bot
from handlers import messages_router
from aiogram.methods import DeleteWebhook
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


#TODO пока задач немного пойдёт и так. Но если их будет много, стоит создать отдельную функцию (или даже класс)
async def main() -> None:
    scheduler = AsyncIOScheduler() # для создания задач, исполняющихся по расписанию

    bot.get_logger().info('Создаю задачу на обновление файла логов')
    scheduler.add_job(bot.get_logger().update_file_handler,
                      trigger=CronTrigger(hour=0, minute=0),
                      id='logger_date_update',
                      replace_existing=True)
    bot.get_logger().info('Задача создана!')

    await bot(DeleteWebhook(drop_pending_updates = True))
    dp.include_routers(messages_router)
    scheduler.start()
    bot.get_logger().info('Запущен планировщик')

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
