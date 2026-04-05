import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import settings
from app.handlers import router


async def main():
    # Логирование нужно, чтобы ты видел ошибки в консоли
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=settings.TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
