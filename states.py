from aiogram.dispatcher.filters.state import State, StatesGroup


class MainForm(StatesGroup):
    menu = State()
    get_schedule = State()
    sub_schedule = State()
