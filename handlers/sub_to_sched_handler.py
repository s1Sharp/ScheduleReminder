from aiogram import types

from bot import dp
from keyboards import sub_to_sched_button_name
from states import MainForm


@dp.message_handler(lambda message: message.text == sub_to_sched_button_name,
                    state="*",
                    content_types=types.ContentTypes.TEXT)
async def cmd_sub_to_sched(message: types.Message):
    await MainForm.sub_schedule.set()
    await message.answer("подписка на расписание stub")


@dp.message_handler(state=[MainForm.sub_schedule],
                    content_types=types.ContentTypes.TEXT)
async def cmd_get_curr_sched(message: types.Message):
    await MainForm.menu.set()
    await message.answer("вы подписаны stub")
