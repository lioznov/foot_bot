import sqlite3


async def init_db():
    conn = sqlite3.connect("database/cafeteria.db")
    cursor = conn.cursor()

    # Таблица меню
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)

    # Таблица пользователей
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            room TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


async def get_user_room(telegram_id: int):
    conn = sqlite3.connect("database/cafeteria.db")
    cursor = conn.cursor()
    cursor.execute("SELECT room FROM users WHERE telegram_id = ?",(telegram_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


async def register_user(telegram_id: int, room: str):
    conn = sqlite3.connect("database/cafeteria.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO users (telegram_id, room) VALUES (?, ?)",(telegram_id,room))
    conn.commit()
    conn.close()


async def get_menu():
    conn = sqlite3.connect("database/cafeteria.db")
    cursor = conn.cursor()
    # 📝 Важно: мы запрашиваем id, name, price
    cursor.execute("SELECT id, name, price FROM menu")
    result = cursor.fetchall()
    conn.close()
    return result



async def add_dish(name: str, price: float):
    conn = sqlite3.connect("database/cafeteria.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO menu (name, price) VALUES (?, ?)", (name, price))
    conn.commit()
    conn.close()


async def clear_menu():
    conn = sqlite3.connect("database/cafeteria.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM menu")
    conn.commit()
    conn.close()