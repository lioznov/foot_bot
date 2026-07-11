import aiosqlite
import os

# Автоматически находим правильный путь к базе данных
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "cafeteria.db")


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        # 1. Создаем таблицу пользователей столовой
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER UNIQUE NOT NULL,
                username TEXT,
                full_name TEXT
            );
        ''')
        # 2. Создаем таблицу актуального меню
        await db.execute('''
            CREATE TABLE IF NOT EXISTS menu (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dish_name TEXT NOT NULL,
                price REAL NOT NULL
            );
        ''')

        # Сохраняем создание таблиц в файл
        await db.commit()