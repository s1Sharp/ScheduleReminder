from aiogram import types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


def add_buttons_to_keyboard(keyboard, buttons):
    for button in buttons:
        keyboard.add(button)


# main menu
main_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
get_cur_sched_button_name = "Получить расписание"
sub_to_sched_button_name = "Подписаться на рассылку расписания"
unsub_from_sched_button_name = "Отписаться от рассылки расписания"
main_menu_buttons = [get_cur_sched_button_name, sub_to_sched_button_name, unsub_from_sched_button_name]
add_buttons_to_keyboard(main_menu_keyboard, main_menu_buttons)

# set subgroup
set_subgroup_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
subgroup1 = "1"
subgroup2 = "2"
subgroup_buttons = [subgroup1, subgroup2]
add_buttons_to_keyboard(set_subgroup_keyboard, subgroup_buttons)

# set day of week
whole_week_button_name = "на всю неделю"
monday_button_name = "понедельник"
tuesday_button_name = "вторник"
wednesday_button_name = "среда"
thursday_button_name = "четверг"
friday_button_name = "пятница"
saturday_button_name = "суббота"

button1 = KeyboardButton(monday_button_name)
button2 = KeyboardButton(tuesday_button_name)
button3 = KeyboardButton(wednesday_button_name)
button4 = KeyboardButton(thursday_button_name)
button5 = KeyboardButton(friday_button_name)
button6 = KeyboardButton(saturday_button_name)

day_of_weeks_keyboard = ReplyKeyboardMarkup().add(KeyboardButton(whole_week_button_name))
day_of_weeks_keyboard.row(button1, button2, button3)
day_of_weeks_keyboard.row(button4, button5, button6)

days_of_week_buttons = [whole_week_button_name, monday_button_name, tuesday_button_name, wednesday_button_name,
                        thursday_button_name, friday_button_name, saturday_button_name]
