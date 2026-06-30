import aiosqlite

DB_PATH = "database/cafeteria.db"
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
        CREATE TABLE IF NOT EXISTS users(
            tg_id INTEGER PRIMERY KEY,
            username TEXT,
            fullname TEXT
        ''')

        await db.execute('''
                    CREATE TABLE IF NOT EXISTS menu (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        dish_name TEXT NOT NULL,
                        price REAL NOT NULL
                    )
                ''')

        await db.execute('''
                    CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tg_id INTEGER,
                        dish_id INTEGER,
                        date TEXT DEFAULT (date('now')),
                        FOREIGN KEY(tg_id) REFERENCES users(tg_id),
                        FOREIGN KEY(dish_id) REFERENCES menu(id)
                    )
                ''')

        await db.commit()