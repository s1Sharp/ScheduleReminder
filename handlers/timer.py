import datetime
import requests
import threading
from xlsxparser import xlsx_parser
from config import API_TOKEN

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
    week_day_number = datetime.datetime.today().weekday()
    week_day_name = day_of_week[week_day_number]
    for chat_id, group_number in nearest_subs:
        schedule = xlsx_parser.storage.get_data_by_group_key(group_number, 1)
        if schedule is not None:
            for text in schedule:
                if text not in xlsx_parser.INVALID_TEXT and week_day_name in text:
                    request = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={chat_id}&text={text}&parse_mode=html"
                    requests.post(request)


class CustomTimer:
    def __init__(self, callback, *args, **kwargs):
        self.t = None
        self.callback = callback

    def set_timer(self, seconds, *args, **kwargs):
        self.t = threading.Timer(seconds, self.callback, args=args, kwargs=kwargs)
        self.t.start()

    def unset_timer(self):
        if self.t is not None:
            self.t.cancel()


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

        if diff_hour > diff_hour_loc >= 0:
            diff_hour = diff_hour_loc
            diff_min = diff_min_loc
        elif diff_hour_loc == diff_hour:
            if diff_min > diff_min_loc >= 0:
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
