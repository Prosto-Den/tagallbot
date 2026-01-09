from bot import dp, bot
from handlers import messages_router, commands_router
from aiogram.methods import DeleteWebhook
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from database.db_manager import DBManager
from database.gif_settings_manager import GIFSettingsSQL


#TODO пока задач немного пойдёт и так. Но если их будет много, стоит создать отдельную функцию (или даже класс)
async def main() -> None:
    scheduler = AsyncIOScheduler() # для создания задач, исполняющихся по расписанию
    bot.get_logger().info('Создаю задачу на обновление файла логов')
    scheduler.add_job(bot.get_logger().update_file_handler,
                      trigger=CronTrigger(hour=0, minute=0),
                      id='logger_date_update',
                      replace_existing=True)
    bot.get_logger().info('Задача создана!')

    await bot(DeleteWebhook(drop_pending_updates=True))

    dp.include_routers(commands_router, messages_router)
    scheduler.start()
    bot.get_logger().info('Запущен планировщик')

    await DBManager.execute(GIFSettingsSQL.CREATE_GIF_SETTINGS_TABLE)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
