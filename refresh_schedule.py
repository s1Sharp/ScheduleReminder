from time import sleep
from threading import Thread

from fetch_xlsx import wget_excel


def refresh_schedule(frequency_time):
    while True:
        wget_excel()
        sleep(frequency_time)


def init_refresh_schedule_job(frequency_time=3600):
    thread = Thread(name="refresh schedule thread", target=refresh_schedule, args=(frequency_time,))
    thread.setDaemon(True)
    thread.start()
