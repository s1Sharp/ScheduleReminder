from aiogram import types

from bot import dp
from keyboards import sub_to_sched_button_name


@dp.message_handler(lambda message: message.text == sub_to_sched_button_name,
                    content_types=types.ContentTypes.TEXT)
async def cmd_sub_to_sched(message: types.Message):
    await message.answer("подписка на расписание stub")
