from aiogram import types

from bot import dp
from keyboards import unsub_from_sched_button_name


@dp.message_handler(lambda message: message.text == unsub_from_sched_button_name,
                    state="*",
                    content_types=types.ContentTypes.TEXT)
async def cmd_sub_to_sched(message: types.Message):
    # TODO del record from db, refresh timer

    await message.answer("у вас не было подписки")
    await message.answer("подписка отменена")
