from aiogram.utils import executor

from bot import dp


def main():
    print('start bot')
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
