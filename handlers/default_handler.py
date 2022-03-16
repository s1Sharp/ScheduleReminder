from aiogram import types
from bot import dp

from keyboards import main_menu_keyboard


@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def cmd_default_handler(message: types.Message):
    await message.answer("извините, не могу разобрать вашу команду", reply_markup=main_menu_keyboard)
