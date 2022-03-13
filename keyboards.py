from aiogram import types


def add_buttons_to_keyboard(keyboard, buttons):
    for button in buttons:
        keyboard.add(button)


main_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_buttons = ["Получить текущее расписание", "Подписаться на рассылку расписания"]
add_buttons_to_keyboard(main_menu_keyboard, main_menu_buttons)
