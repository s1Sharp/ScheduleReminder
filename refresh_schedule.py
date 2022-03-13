from time import sleep
from threading import Thread
import logging

from fetch_xlsx import wget_excel


def refresh_schedule(frequency_time):
    while True:
        wget_excel()
        logging.info("schedule file updated")
        sleep(frequency_time)


def init_refresh_schedule_job(frequency_time=3600):
    thread = Thread(name="RefreshScheduleThread", target=refresh_schedule, args=(frequency_time,))
    thread.setDaemon(True)
    thread.start()
