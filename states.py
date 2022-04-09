from aiogram.dispatcher.filters.state import State, StatesGroup


class MainForm(StatesGroup):
    menu = State()
    set_subgroup = State()
    set_day_of_week = State()
    get_schedule = State()
    set_time = State()
    sub_schedule = State()
