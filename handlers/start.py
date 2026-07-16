from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from database.db import get_menu

router = Router()

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🍽 Посмотреть меню")]
    ],
    resize_keyboard=True
)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! Добро пожаловать в нашу столовую. "
        f"Нажми на кнопку ниже, чтобы увидеть меню на сегодня 👇",
        reply_markup=menu_keyboard
    )


@router.message(F.text == "🍽 Посмотреть меню")
async def show_menu(message: Message):
    menu_items = await get_menu()
    if not menu_items:
        await message.answer("Извините, меню на сегодня пока пусто 😔")
        return

    response = "📝 **Меню на сегодня:**\n\n"
    for name, price in menu_items:
        response += f"🔹 {name} — {price} руб.\n"

    await message.answer(response, parse_mode="Markdown")