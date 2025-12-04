from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


class Scheduler:
    """
    Класс для создания задач, исполняющихся по расписанию
    """
    __scheduler = AsyncIOScheduler()


