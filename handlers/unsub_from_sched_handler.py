from aiogram import types
from xlsxparser import xlsx_parser
from bot import dp
import datetime
from keyboards import unsub_from_sched_button_name
from handlers.timer import get_nearest_subs, CUSTOM_TIMER


@dp.message_handler(lambda message: message.text == unsub_from_sched_button_name,
                    state="*",
                    content_types=types.ContentTypes.TEXT)
async def cmd_sub_to_sched(message: types.Message):
    # TODO del record from db, refresh timer

    # xlsx_parser.storage.data_subscriptions(group_key=group_number, tg_id=str(message.chat.id), time=time,
    #                                        action='add')
    #
    # subs = xlsx_parser.storage.get_subscriptions()
    # nearest_subs, min_hour_diff, min_minute_diff = get_nearest_subs(subs)
    #
    # delta_seconds = datetime.timedelta(hours=min_hour_diff, minutes=min_minute_diff).total_seconds()
    # CUSTOM_TIMER.unset_timer()
    # CUSTOM_TIMER.set_timer(delta_seconds, nearest_subs)

    await message.answer("у вас не было подписки")
    await message.answer("подписка отменена")
