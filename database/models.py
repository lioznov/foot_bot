import aiosqlite
from database.db import DB_PATH

async def register_user(tg_id: int, username: str, full_name: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (tg_id, username, full_name) VALUES (?, ?, ?)",
            (tg_id, username, full_name)
        )
        await db.commit()


async def update_menu_in_db(menu_items: list[tuple[str, float]]):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM menu")

        await db.executemany(
            "INSERT INTO menu (dish_name, price) VALUES (?, ?)",
            menu_items
        )
        await db.commit()