from aiogram import types

from bot import dp
from keyboards import get_cur_sched_button_name, main_menu_keyboard, set_subgroup_keyboard, whole_week_button_name, \
    days_of_week_buttons, \
    day_of_weeks_keyboard
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
    await MainForm.set_day_of_week.set()
    state = dp.get_current().current_state()
    await state.update_data(group_number=message.text)
    await message.answer("введите номер подгруппы", reply_markup=set_subgroup_keyboard)


def is_valid_subgroup_number(subgroup_number):
    return subgroup_number in ['1', '2']


@dp.message_handler(lambda message: is_valid_subgroup_number(message.text),
                    state=[MainForm.set_day_of_week],
                    content_types=types.ContentTypes.TEXT)
async def cmd_get_curr_sched(message: types.Message):
    await MainForm.get_schedule.set()
    state = dp.get_current().current_state()
    await state.update_data(subgroup_number=message.text)
    await message.answer("выберите день недели или всю неделю", reply_markup=day_of_weeks_keyboard)


@dp.message_handler(lambda message: not is_valid_subgroup_number(message.text),
                    state=[MainForm.set_day_of_week],
                    content_types=types.ContentTypes.TEXT)
async def cmd_incorrect_subgroup_number(message: types.Message):
    await MainForm.menu.set()
    await message.reply("неверный номер подгруппы", reply_markup=main_menu_keyboard)


@dp.message_handler(lambda message: message.text in days_of_week_buttons,
                    state=[MainForm.get_schedule],
                    content_types=types.ContentTypes.TEXT)
async def cmd_get_curr_sched(message: types.Message):
    await MainForm.menu.set()
    state = dp.get_current().current_state()
    data = await state.get_data()
    group_number = data['group_number']
    subgroup_number = data['subgroup_number']
    day_of_week_name = message.text

    day_str = f"<strong>Расписание для группы {group_number}</strong>\n\n"
    day_str_printed = False
    schedule = xlsx_parser.storage.get_data_by_group_key(group_number, subgroup_number)
    if schedule is not None:
        for text in schedule:
            if text not in xlsx_parser.INVALID_TEXT:
                if day_of_week_name in text or day_of_week_name == whole_week_button_name:
                    if not day_str_printed:
                        await message.answer(day_str, parse_mode='html', reply_markup=main_menu_keyboard)
                        day_str_printed = True
                    await message.answer(text, parse_mode='html', reply_markup=main_menu_keyboard)
    else:
        await message.answer("произошел сбой в базе данных, извиняемся за неудобства", reply_markup=main_menu_keyboard)


@dp.message_handler(lambda message: message.text not in days_of_week_buttons,
                    state=[MainForm.get_schedule],
                    content_types=types.ContentTypes.TEXT)
async def cmd_incorrect_day_of_week(message: types.Message):
    await MainForm.menu.set()
    await message.reply("неверный день недели", reply_markup=main_menu_keyboard)


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
        await message.reply("номер группы не существует",
                            reply_markup=main_menu_keyboard)
