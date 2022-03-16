import re
from aiogram import types

from bot import dp
from keyboards import get_cur_sched_button_name, main_menu_keyboard, set_subgroup_keyboard
from states import MainForm
from xlsxparser import xlsx_parser
from xlsxparser import xlsx_env

INVALID_TEXT = ['\n', '', None]

@dp.message_handler(lambda message: message.text == get_cur_sched_button_name,
                    state="*",
                    content_types=types.ContentTypes.TEXT)
async def cmd_get_curr_sched(message: types.Message):
    await MainForm.set_subgroup.set()
    await message.answer("введите номер группы",reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(lambda message: is_valid_group_number(message.text),
                    state=[MainForm.set_subgroup],
                    content_types=types.ContentTypes.TEXT)
async def cmd_get_curr_sched(message: types.Message):
    await MainForm.get_schedule.set()
    state = dp.get_current().current_state()
    await state.update_data(group_number=message.text)
    await message.answer("введите номер подгруппы", reply_markup=set_subgroup_keyboard)

def is_valid_group_number(group_number):
    fixed_groups = [elem.split(' ')[0] for elem in xlsx_env.dgroup]
    return re.match(r"^\d{2}-\d{3}$", group_number) and (group_number in fixed_groups)

@dp.message_handler(state=[MainForm.get_schedule],
                    content_types=types.ContentTypes.TEXT)
async def cmd_get_curr_sched(message: types.Message):
    await MainForm.menu.set()
    state = dp.get_current().current_state()
    group_number = await state.get_data()
    subgroup_number = message.text
    schedule = xlsx_parser.storage.get_data_by_group_key(group_number['group_number'], subgroup_number)
    schedule = schedule.split(xlsx_env.KEY_WORD_NEXT_DAY)
    for text in schedule:
        if text not in INVALID_TEXT:
            await message.answer(text, parse_mode='html', reply_markup=main_menu_keyboard)
        


@dp.message_handler(lambda message: not is_valid_group_number(message.text),
                    state=[MainForm.set_subgroup],
                    content_types=types.ContentTypes.TEXT)
async def cmd_incorrect_group_number(message: types.Message):
    await MainForm.menu.set()
    await message.reply("номер группы некорректен, требуется следующий формат\n <b>xx-xxx</b>", parse_mode='html', reply_markup=main_menu_keyboard)
