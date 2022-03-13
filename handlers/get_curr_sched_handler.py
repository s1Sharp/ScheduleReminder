from aiogram import types

from bot import dp
from keyboards import get_cur_sched_button_name


@dp.message_handler(lambda message: message.text == get_cur_sched_button_name,
                    content_types=types.ContentTypes.TEXT)
async def cmd_get_curr_sched(message: types.Message):
    await message.answer("текущее расписание stub")
