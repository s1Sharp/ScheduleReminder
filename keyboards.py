from aiogram import types


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
