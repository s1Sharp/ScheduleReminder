import datetime
import logging

import requests
import threading
from xlsxparser import xlsx_parser
from config import API_TOKEN
import asyncio

day_of_week = {
    0: 'понедельник',
    1: 'вторник',
    2: 'среда',
    3: 'четверг',
    4: 'пятница',
    5: 'суббота',
    6: 'воскресеньe',
}


def cb_impl(*args):
    nearest_subs = args[0]
    logging.info(nearest_subs)
    week_day_number = datetime.datetime.today().weekday()
    week_day_name = day_of_week[week_day_number]

    for chat_id, group_number in nearest_subs:
        day_str = f"<strong>Расписание для группы {group_number}</strong>\n\n"
        schedule = xlsx_parser.storage.get_data_by_group_key(group_number, 1)
        if schedule is not None:
            for text in schedule:
                if text not in xlsx_parser.INVALID_TEXT:
                    if week_day_name in text:
                        request = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={chat_id}&text={day_str}&parse_mode=html"
                        requests.post(request)
                        request = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={chat_id}&text={text}&parse_mode=html"
                        requests.post(request)
                    else:
                        empty_day_str = "На сегодняшний день нет расписания"
                        request = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={chat_id}&text={empty_day_str}&parse_mode=html"
                        requests.post(request)
                        break


class CustomTimer:
    def __init__(self, callback, *args, **kwargs):
        self.t = None
        self.callback = callback

    def update_timer(self):
        subs = xlsx_parser.storage.get_subscriptions()
        nearest_subs, min_hour_diff, min_minute_diff = get_nearest_subs(subs)

        delta_seconds = datetime.timedelta(hours=min_hour_diff, minutes=min_minute_diff).total_seconds() \
                        - datetime.timedelta(seconds=datetime.datetime.now().second).total_seconds()
        # remove delta second time, it will callback everytime on start minute
        self.unset_timer()
        self.set_timer(delta_seconds, nearest_subs)

    def set_timer(self, seconds, *args, **kwargs):
        self.t = threading.Timer(seconds, self.callback, args=args, kwargs=kwargs)
        self.t.start()
        logging.info(f"Set timer, callback will be invoked in {seconds} seconds")

    def unset_timer(self):
        if self.t is not None:
            self.t.cancel()
            logging.info("Unset timer")


CUSTOM_TIMER = CustomTimer(cb_impl)


def get_nearest_subs(subs):
    diff_hour = 24
    diff_min = 60
    curr_time = datetime.datetime.now()
    curr_hour, curr_min = curr_time.hour, curr_time.minute
    for sub in subs:
        time = sub[0]
        date_time_obj = datetime.datetime.strptime(time, "%H:%M")
        hour, minute = date_time_obj.hour, date_time_obj.minute

        diff_hour_loc = hour - curr_hour
        diff_min_loc = minute - curr_min
        if (diff_hour_loc * 60 + diff_min_loc) <= 0:
            diff_hour_loc = 23 - curr_hour + hour
            diff_min_loc = 60 - curr_min + minute

        if diff_hour > diff_hour_loc >= 0:
            diff_hour = diff_hour_loc
            diff_min = diff_min_loc
        elif diff_hour_loc == diff_hour:
            if diff_min > diff_min_loc > 0:
                diff_min = diff_min_loc

    result = []
    for sub in subs:
        time = sub[0]
        date_time_obj = datetime.datetime.strptime(time, "%H:%M")
        hour, minute = date_time_obj.hour, date_time_obj.minute
        diff_hour_loc = hour - curr_hour
        diff_min_loc = minute - curr_min

        if diff_hour_loc == diff_hour and diff_min_loc == diff_min:
            result.append((sub[1], sub[2]))

    return result, diff_hour, diff_min
