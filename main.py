import asyncio
import logging
import os
import sys

os.environ["HTTP_PROXY"] = "http://127.0.0.1:2081"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:2081"

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from config import BOT_TOKEN
from database.db import init_db
from aiogram import Bot, Dispatcher

from handlers.start import router as start_router
from handlers.admin import router as admin_router

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def on_startup():
    print("Бот успешно запущен и готов к работе!")
    await init_db()
    print("База данных успешно инициализирована!")


async def main():
    dp.startup.register(on_startup)

    dp.include_router(start_router)
    dp.include_router(admin_router)

    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("----- Бот остановлен! -----")