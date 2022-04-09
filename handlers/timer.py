import datetime
import time
import asyncio
import threading
import bot
import os
API_TOKEN = os.environ["SR_BOT_TOKEN"]
from xlsxparser import xlsx_parser
import requests



def get_nearest_subs(subs):
    curr_time = datetime.datetime.now()
    curr_hour, curr_min = curr_time.hour, curr_time.minute

    result = []
    for sub in subs:
        time = sub[0]
        date_time_obj = datetime.datetime.strptime(time, "%H:%M")
        hour, minute = date_time_obj.hour, date_time_obj.minute

        if curr_hour == hour and curr_min == minute:
            result.append((sub[1], sub[2]))

    return result


def poll_subs():
    while True:
        subs = xlsx_parser.storage.get_subscriptions()
        nearest_subs = get_nearest_subs(subs)

        for chat_id, group_number in nearest_subs:
            schedule = xlsx_parser.storage.get_data_by_group_key(group_number, 1)
            if schedule is not None:
                for text in schedule:
                    if text not in xlsx_parser.INVALID_TEXT:
                        request = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={chat_id}&text={text}&parse_mode=html"
                        requests.post(request)
                        # loop = asyncio.new_event_loop()
                        # asyncio.set_event_loop(loop)
                        # loop.run_until_complete(bot.bot.send_message(chat_id=chat_id, text=text, parse_mode='html'))
                        # await loop.run_until_complete(bot.bot.send_message(chat_id=chat_id, text=text, parse_mode='html'))
                        # loop.close()
                        # loop = asyncio.get_event_loop()
                        # now = loop.time()
                        
                        # async with asyncio.timeout( 2.5 ):
                        # await (bot.bot.send_message(chat_id=chat_id, text=text, parse_mode='html'), 3.5)
        time.sleep(60)


def bg_async(poll_subs):
    def wrapper():
        loop = asyncio.new_event_loop()
        loop.run_until_complete(poll_subs)

    threading.Thread(target=wrapper).start()


def main_thread():
    bg_async(poll_subs())


def init_poll_subs_job():
    thread = threading.Thread(target=main_thread, name="pollSubsThread")
    thread.setDaemon(True)
    thread.start()
