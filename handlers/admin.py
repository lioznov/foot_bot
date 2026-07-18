from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from config import ADMIN_ID
from database.db import add_dish, clear_menu

router = Router()

def is_admin(user_id: int) -> bool:
    return str(user_id) == str(ADMIN_ID)



@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("У вас нет прав доступа к этой команде ❌")
        return

    await message.answer(
        "Добро пожаловать в панель управления!\n\n"
        "Команды для управления меню: \n"
        "➕ '/add_dish [Название блюда] [Цена]' - добавить блюдо в меню\n"
        "❌ '/clear_menu' - полностью очистить меню на сегодня",
        parse_mode="HTML"
    )



@router.message(Command("add_dish"))
async def cmd_add_dish(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("У вас нет прав доступа к этой команде ❌")
        return

    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.answer("Ошибка! Правильный формат: '/add_dish Картошка 120' ⚠️", parse_mode="Markdown")
        return

    name = args[1]
    try:
        price = float(args[2])
    except ValueError:
        await message.answer("Ошибка! Цена должна быть числом ⚠️")
        return

    await add_dish(name, price)
    await message.answer(f"✅ Блюдо **{name}** ({price} руб.) успешно добавлено в меню!" , parse_mode="Markdown")



@router.message(Command("clear_menu"))
async def cmd_clear_menu(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("У вас нет прав доступа к этой команде ❌")
        return

    await clear_menu()
    await message.answer("🧹 Меню успешно очищено! Теперь база данных пуста.")



@router.callback_query(F.data.startswith("accept_order"))
async def accept_order(callback: CallbackQuery,bot):
    user_id = int(callback.data.split("_")[2])

    clean_text = callback.message.text.replace("**","")
    await callback.message.edit_text(
        text=clean_text + "\n\n 🟢 <b>Заказ принят и готовиться!</b>",
        parse_mode="HTML"
    )

    try:
        await bot.send_message(
            chat_id=user_id,
            text="<b>Ваш заказ принят столовой и уже готовиться!</b> Скоро все будет готово. Приятного аппетита!",
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Не удалось уведомить пользователя {user_id}: {e}")

    await callback.answer(text="Заказ успешно принят!")


@router.callback_query(F.data.startswith("reject_order_"))
async def reject_order(callback: CallbackQuery, bot):
    user_id = int(callback.data.split("_")[2])

    clean_text = callback.message.text.replace("**", "")
    await callback.message.edit_text(
        text=clean_text + "\n\n🔴 <b>Заказ отклонен.</b>",
        parse_mode="HTML"
    )

    try:
        await bot.send_message(
            chat_id=user_id,
            text="❌ <b>К сожалению, ваш заказ был отклонен столовой.</b> Обратитесь к администратору.",
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Не удалось уведомить пользователя {user_id}: {e}")

    await callback.answer(text="Заказ отклонен. ❌")

