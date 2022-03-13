from aiogram import types

from bot import dp
from keyboards import main_menu_keyboard


@dp.message_handler(state="*", commands="start")
async def cmd_start(message: types.Message):
    await message.answer(
        "Здравствуйте, вас приветствует бот! "
        "Вы можете получить текущее расписание, а также подписаться на ежедневную рассылку расписания, "
        "для этого нажмите на соответствующую кнопку.", reply_markup=main_menu_keyboard)
