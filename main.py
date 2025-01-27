import asyncio

from aiogram import Dispatcher
from bot import bot
from handlers import router
from loggers import error_logger


dp = Dispatcher()


@error_logger
async def main() -> None:
    """
    Запуск бота
    :return:
    """
    dp.include_router(router)
    await dp.start_polling(bot)


# Основная точка входа
if __name__ == "__main__":
    asyncio.run(main())
