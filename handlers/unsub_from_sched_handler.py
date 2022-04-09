from aiogram import types
from xlsxparser import xlsx_parser
from bot import dp
import logging
import datetime
from keyboards import unsub_from_sched_button_name
from handlers.timer import get_nearest_subs, CUSTOM_TIMER


@dp.message_handler(lambda message: message.text == unsub_from_sched_button_name,
                    state="*",
                    content_types=types.ContentTypes.TEXT)
async def cmd_sub_to_sched(message: types.Message):
    remove_action = xlsx_parser.storage.data_subscriptions(group_key=None, tg_id=str(message.chat.id), time=None,
                                                           action='remove')
    logging.info(f"db unsubscribe sub with tg_id {message.chat.id}")

    CUSTOM_TIMER.update_timer()

    if remove_action:
        await message.answer("подписка отменена")
    else:
        await message.answer("у вас не было подписки")