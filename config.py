import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("ОШИБКА: Переменная не была найдена!")
try:
    ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
except ValueError:
    raise ValueError("ОШИБКА: Переменная ADMIN_ID, олжна быть числом!")