import re
from aiogram import types

from bot import dp
from keyboards import get_cur_sched_button_name
from states import MainForm
from xlsxparser import xlsxparser


@dp.message_handler(lambda message: message.text == get_cur_sched_button_name,
                    state="*",
                    content_types=types.ContentTypes.TEXT)
async def cmd_get_curr_sched(message: types.Message):
    await MainForm.get_schedule.set()
    await message.answer("введите номер группы")


def is_valid_group_number(group_number):
    return re.match(r"^\d{2}-\d{3}$", group_number)


@dp.message_handler(lambda message: is_valid_group_number(message.text),
                    state=[MainForm.get_schedule],
                    content_types=types.ContentTypes.TEXT)
async def cmd_get_curr_sched(message: types.Message):
    await MainForm.menu.set()
    group_number = message.text
    schedule = xlsxparser.storage.get_data_by_group_key(group_number)
    await message.answer(schedule, parse_mode="html")


@dp.message_handler(lambda message: not is_valid_group_number(message.text),
                    state=[MainForm.get_schedule],
                    content_types=types.ContentTypes.TEXT)
async def cmd_incorrect_group_number(message: types.Message):
    await MainForm.menu.set()
    await message.reply("номер группы некорректен, требуется следующий формат xx-xxx")
