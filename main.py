from aiogram.utils import executor

from bot import dp
import handlers
from fetch_xlsx import wget_excel


def main():
    print("start bot")
    wget_excel()
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
