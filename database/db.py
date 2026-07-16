import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cafeteria.db")

async def init_db():
    """Инициализация базы данных и создание таблицы меню"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    # Добавим стартовое меню, если таблица пустая
    cursor.execute("SELECT COUNT(*) FROM menu")
    if cursor.fetchone()[0] == 0:
        start_menu = [
            ("Борщ домашний", 150.0),
            ("Пюре картофельное", 80.0),
            ("Котлета куриная", 110.0),
            ("Компот из сухофруктов", 40.0)
        ]
        cursor.executemany("INSERT INTO menu (name, price) VALUES (?, ?)", start_menu)
        conn.commit()
    conn.close()

async def get_menu():
    """Получение всех блюд из меню"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, price FROM menu")
    rows = cursor.fetchall()
    conn.close()
    return rows

async def add_dish(name: str, price: float):
    """Добавление нового блюда"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO menu (name, price) VALUES (?, ?)", (name, price))
    conn.commit()
    conn.close()

async def clear_menu():
    """Полная очистка меню"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM menu")
    conn.commit()
    conn.close()