from aiogram import types

from bot import dp
from keyboards import get_cur_sched_button_name, main_menu_keyboard, set_subgroup_keyboard
from states import MainForm
from xlsxparser import xlsx_parser
from handlers.handler_utils import is_valid_group_number, is_valid_existing_group_number


@dp.message_handler(lambda message: message.text == get_cur_sched_button_name,
                    state="*",
                    content_types=types.ContentTypes.TEXT)
async def cmd_get_curr_sched(message: types.Message):
    await MainForm.set_subgroup.set()
    await message.answer("введите номер группы", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(
    lambda message: is_valid_group_number(message.text) and is_valid_existing_group_number(message.text),
    state=[MainForm.set_subgroup],
    content_types=types.ContentTypes.TEXT)
async def cmd_get_curr_sched(message: types.Message):
    await MainForm.get_schedule.set()
    state = dp.get_current().current_state()
    await state.update_data(group_number=message.text)
    await message.answer("введите номер подгруппы", reply_markup=set_subgroup_keyboard)


@dp.message_handler(state=[MainForm.get_schedule],
                    content_types=types.ContentTypes.TEXT)
async def cmd_get_curr_sched(message: types.Message):
    await MainForm.menu.set()
    state = dp.get_current().current_state()
    data = await state.get_data()
    subgroup_number = message.text
    schedule = xlsx_parser.storage.get_data_by_group_key(data['group_number'], subgroup_number)
    if schedule is not None:
        for text in schedule:
            if text not in xlsx_parser.INVALID_TEXT:
                await message.answer(text, parse_mode='html', reply_markup=main_menu_keyboard)
    else:
        await message.answer("произошел сбой в базе данных, извиняемся за неудобства", reply_markup=main_menu_keyboard)


@dp.message_handler(
    lambda message: not is_valid_group_number(message.text) or not is_valid_existing_group_number(message.text),
    state=[MainForm.set_subgroup],
    content_types=types.ContentTypes.TEXT)
async def cmd_incorrect_group_number(message: types.Message):
    await MainForm.menu.set()
    if not is_valid_group_number(message.text):
        await message.reply("номер группы некорректен, требуется следующий формат\n <b>xx-xxx</b>", parse_mode='html',
                            reply_markup=main_menu_keyboard)
    else:
        await message.reply("номер группы не существуsет",
                            reply_markup=main_menu_keyboard)
