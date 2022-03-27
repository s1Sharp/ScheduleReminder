from aiogram import types

from bot import dp
from keyboards import main_menu_keyboard, sub_to_sched_button_name
from states import MainForm
from handlers.handler_utils import is_valid_group_number, is_valid_time


@dp.message_handler(lambda message: message.text == sub_to_sched_button_name,
                    state="*",
                    content_types=types.ContentTypes.TEXT)
async def cmd_sub_to_sched(message: types.Message):
    await MainForm.set_time.set()
    await message.answer("введите номер группы", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: is_valid_group_number(message.text),
                    state=[MainForm.set_time],
                    content_types=types.ContentTypes.TEXT)
async def cmd_sub_to_sched(message: types.Message):
    await MainForm.sub_schedule.set()
    state = dp.get_current().current_state()
    await state.update_data(group_number=message.text)
    await message.answer("введите время в формате <b>hh:mm</b>", parse_mode='html')


@dp.message_handler(lambda message: not is_valid_group_number(message.text),
                    state=[MainForm.set_time],
                    content_types=types.ContentTypes.TEXT)
async def cmd_incorrect_group_number(message: types.Message):
    await MainForm.menu.set()
    await message.reply("номер группы некорректен, требуется следующий формат\n <b>xx-xxx</b>", parse_mode='html',
                        reply_markup=main_menu_keyboard)


@dp.message_handler(lambda message: is_valid_time(message.text),
                    state=[MainForm.sub_schedule],
                    content_types=types.ContentTypes.TEXT)
async def cmd_sub_to_sched(message: types.Message):
    await MainForm.menu.set()
    state = dp.get_current().current_state()
    data = await state.get_data()
    group_number = data['group_number']
    time = message.text

    # TODO fetch db subs, update timer

    await message.answer(f"подписка активирована, рассылка расписания будет происходит каждый день в {time}",
                         reply_markup=main_menu_keyboard)


@dp.message_handler(lambda message: not is_valid_time(message.text),
                    state=[MainForm.sub_schedule],
                    content_types=types.ContentTypes.TEXT)
async def cmd_invalid_time(message: types.Message):
    await MainForm.menu.set()
    await message.reply("время введено в некорректном формате, требуется следующий формат <b>hh:mm</b>",
                        parse_mode='html', reply_markup=main_menu_keyboard)
