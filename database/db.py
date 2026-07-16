import sqlite3

async def init_db():
    conn = sqlite3.connect("database/cafeteria.db")
    cursor = conn.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu (
                id INTEGER PRIMERY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
    """)

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
    cursor.execute("SELECT room FROM users WHERE telegram_id = ?",(telegram_id))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

async def register_user(telegram_id: int, room: str):
    conn = sqlite3.connect("database/cafeteria.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO users (telegram_id, room) VALUES (?, ?)",(telegram_id,room))
    conn.commit()
    conn.close()
