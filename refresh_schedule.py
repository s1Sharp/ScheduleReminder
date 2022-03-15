import os
import random
from time import sleep
from threading import Thread
import logging
import hashlib
from pathlib import Path

from xlsxparser.xlsxparser import update_schedule_db
from fetch_xlsx import wget_excel
from config import SCHEDULE_PATH, NEW_SCHEDULE_PATH


def get_md5_hash(file):
    md5 = hashlib.md5()
    try:
        with open(file, "rb") as file:
            while True:
                data = file.read(65536)
                if not data:
                    break
                md5.update(data)
    except IOError as e:
        logging.info(str(e))
        return None
    return md5.hexdigest()


def is_schedule_updated():
    wget_excel(NEW_SCHEDULE_PATH)

    old_hash = get_md5_hash(SCHEDULE_PATH)
    if old_hash is None:
        return False
    new_hash = get_md5_hash(NEW_SCHEDULE_PATH)
    if new_hash is None:
        return False

    return old_hash != new_hash


def refresh_schedule(frequency_time):
    file = Path(SCHEDULE_PATH)
    if not file.is_file():
        wget_excel(SCHEDULE_PATH)
        update_schedule_db()
        logging.info("schedule updated")
        sleep(random.uniform(5, 10))
    while True:
        updated = is_schedule_updated()
        if updated:
            logging.info("schedule updating")
            try:
                file = os.path.join(SCHEDULE_PATH)
                os.remove(file)
                os.rename(NEW_SCHEDULE_PATH, SCHEDULE_PATH)
            except FileNotFoundError as e:
                logging.info(str(e))
            # update DB here
            # TODO: mutex for SCHEDULE_PATH
            update_schedule_db()
            logging.info("schedule updated")
        else:
            logging.info("schedule not updated")
            try:
                os.remove(NEW_SCHEDULE_PATH)
            except FileNotFoundError as e:
                logging.info(str(e))
        sleep(frequency_time)


def init_refresh_schedule_job(frequency_time=3600):
    thread = Thread(name="RefreshScheduleThread", target=refresh_schedule, args=(frequency_time,))
    thread.setDaemon(True)
    thread.start()
