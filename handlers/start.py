from aiogram import Router, types
from aiogram.start import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Посмотреть меню"))
    await message.answer(
        f"Привет, {message.from_user.full_name}!\n"
        f"Добро пожаловать в бота нашей столовой...",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )