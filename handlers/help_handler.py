from aiogram import types

from bot import dp


@dp.message_handler(state='*', commands='help')
async def cmd_help(message: types.Message):
    await message.answer(
        "Вы можете получить текущее расписание, а также подписаться на ежедневную рассылку расписания, "
        "для этого нажмите на соответствующую кнопку.")
