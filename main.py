from aiogram.utils import executor

import logging
from bot import dp
import handlers
from log import setup_logging
from refresh_schedule import init_refresh_schedule_job
from config import SCHEDULE_UPDATE_FREQUENCY_SEC
import handlers.timer


def main():
    setup_logging()
    handlers.timer.init_poll_subs_job()
    logging.info("init bot")
    init_refresh_schedule_job(SCHEDULE_UPDATE_FREQUENCY_SEC)
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
