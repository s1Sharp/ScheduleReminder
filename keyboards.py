from aiogram import types


def add_buttons_to_keyboard(keyboard, buttons):
    for button in buttons:
        keyboard.add(button)


# main menu
main_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
get_cur_sched_button_name = "Получить текущее расписание"
sub_to_sched_button_name = "Подписаться на рассылку расписания"
main_menu_buttons = [get_cur_sched_button_name, sub_to_sched_button_name]
add_buttons_to_keyboard(main_menu_keyboard, main_menu_buttons)
