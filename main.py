from aiogram.utils import executor

from bot import dp
import handlers
from refresh_schedule import init_refresh_schedule_job
from config import SCHEDULE_UPDATE_FREQUENCY_SEC


def main():
    print("start bot")
    init_refresh_schedule_job(SCHEDULE_UPDATE_FREQUENCY_SEC)
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
