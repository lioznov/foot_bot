from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from config import ADMIN_ID
from database.db import add_dish, clear_menu

router = Router()


def is_admin(user_id: int) -> bool:
    """Проверка, является ли пользователь администратором"""
    return str(user_id) == str(ADMIN_ID)


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("У вас нет прав доступа к этой команде ❌")
        return

    await message.answer(
        "👋 Добро пожаловать в панель управления столовой!\n\n"
        "Команды для управления меню:\n"
        "➕ `/add_dish [Название] [Цена]` — добавить блюдо в меню\n"
        "❌ `/clear_menu` — полностью очистить меню на сегодня",
        parse_mode="Markdown"
    )


@router.message(Command("add_dish"))
async def cmd_add_dish(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("У вас нет прав доступа к этой команде ❌")
        return

    # Извлекаем аргументы команды
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.answer("Ошибка! Правильный формат: `/add_dish Картошка 120` ⚠️", parse_mode="Markdown")
        return

    name = args[1]
    try:
        price = float(args[2])
    except ValueError:
        await message.answer("Ошибка! Цена должна быть числом ⚠️")
        return

    await add_dish(name, price)
    await message.answer(f"✅ Блюдо **{name}** ({price} руб.) успешно добавлено в меню!", parse_mode="Markdown")


@router.message(Command("clear_menu"))
async def cmd_clear_menu(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("У вас нет прав доступа к этой команде ❌")
        return

    await clear_menu()
    await message.answer("🧹 Меню успешно очищено! Теперь база данных пуста.")