from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database.db import get_menu, get_user_room, register_user

# 💥 ДОБАВИЛИ ИМПОРТЫ НАСТРОЕК И КЛАВИАТУРЫ АДМИНА
from config import ADMIN_ID
from keyboards.admin_keyboards import get_order_management_keyboard

router = Router()
user_carts = {}


# Функция-генератор кнопок меню
def get_inline_menu(menu_items):
    keyboard_buttons = []

    # Проходимся по каждому блюду, которое достали из базы
    for item_id, name, price in menu_items:
        # Создаем кнопку для каждого блюда
        button = InlineKeyboardButton(
            text=f"➕ {name} ({price} руб.)",
            callback_data=f"add_{item_id}"  # При клике бот получит сигнал, например: "add_1"
        )
        keyboard_buttons.append([button])  # Добавляем кнопку на новую строчку

    # В самом низу списка кнопок делаем большую кнопку подтверждения заказа
    confirm_button = InlineKeyboardButton(
        text="✅ Оформить заказ",
        callback_data="confirm_order"
    )
    keyboard_buttons.append([confirm_button])

    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


class Registration(StatesGroup):
    waiting_for_room = State()


menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🍽️ Посмотреть меню")]
    ],
    resize_keyboard=True
)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    room = await get_user_room(user_id)

    if room:
        await message.answer(
            f"Рады видеть вас снова, гость из комнаты {room}! \n"
            f"Нажмите на кнопку ниже, чтобы увидеть меню на сегодня",
            reply_markup=menu_keyboard
        )
    else:
        await message.answer(
            f"Привет, {message.from_user.first_name}! Добро пожаловать в наш отель."
            f"Пожалуйста, введите **номер вашей комнаты** (например: 305 или 12А), "
            f"чтобы мы могли принимать ваши заказы на завтрак:"
        )
        await state.set_state(Registration.waiting_for_room)


@router.message(Registration.waiting_for_room)
async def process_room_input(message: Message, state: FSMContext):
    room_number = message.text.strip()

    if len(room_number) > 10:
        await message.answer("Номер комнаты выглядит слишком длинным. Попробуйте еще раз!")
        return

    await register_user(message.from_user.id, room_number)
    await state.clear()

    await message.answer(
        f"Отлично! Комната {room_number} успешно зарегистрирована. ✅\n"
        f"Теперь вы можете смотреть меню и делать заказы на завтрак!",
        reply_markup=menu_keyboard
    )


# Обработка кнопки просмотра меню
@router.message(F.text == "🍽️ Посмотреть меню")
async def show_menu(message: Message):
    room = await get_user_room(message.from_user.id)
    if not room:
        await message.answer("Пожалуйста, сначала введите /start, чтобы зарегистрировать комнату.")
        return

    # Получаем меню из базы (id, name, price)
    menu_items = await get_menu()
    if not menu_items:
        await message.answer("Извините, меню на завтрак пока пусто 😔")
        return

    response = "📝 **Меню завтраков на сегодня:**\n\nВыбирайте блюда, нажимая на кнопки ниже 👇"

    # Генерируем клавиатуру с кнопками из базы данных
    reply_markup = get_inline_menu(menu_items)

    # Отправляем сообщение с клавиатурой
    await message.answer(response, reply_markup=reply_markup, parse_mode="Markdown")


# 💥 НОВЫЙ ХЕНДЛЕР 1: Ловим нажатие на кнопки добавления блюд
@router.callback_query(F.data.startswith("add_"))
async def add_to_cart(callback: CallbackQuery):
    user_id = callback.from_user.id

    # Из callback_data (например, "add_3") достаем ID блюда (3)
    dish_id = int(callback.data.split("_")[1])

    # Если у пользователя еще нет корзины, создаем пустой список
    if user_id not in user_carts:
        user_carts[user_id] = []

    # Добавляем ID блюда в корзину
    user_carts[user_id].append(dish_id)

    # Показываем быстрое всплывающее уведомление вверху экрана
    await callback.answer(text="Добавлено в ваш заказ! 🍳", show_alert=False)


# 💥 НОВЫЙ ХЕНДЛЕР 2: Ловим нажатие на кнопку "Оформить заказ"
@router.callback_query(F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, bot):
    user_id = callback.from_user.id

    # Проверка на пустую корзину
    if user_id not in user_carts or not user_carts[user_id]:
        await callback.answer(text="Вы не выбрали ни одного блюда! ❌", show_alert=True)
        return

    room = await get_user_room(user_id)
    menu_items = await get_menu()
    menu_dict = {item[0]: (item[1], item[2]) for item in menu_items}

    order_details = []
    total_price = 0.0

    # Собираем текстовые строчки для чека
    for dish_id in user_carts[user_id]:
        if dish_id in menu_dict:
            name, price = menu_dict[dish_id]
            order_details.append(f"• {name} — {price} руб.")
            total_price += price

    # Отправляем сообщение гостю
    user_text = (
            f"📋 **Ваш заказ отправлен на кухню!**\n\n"
            f"🚪 **Комната:** {room}\n"
            f"🥞 **Выбранные блюда:**\n" + "\n".join(order_details) + f"\n\n"
                                                                     f"💰 **Итого к оплате:** {total_price} руб.\n\n"
                                                                     f"⏳ Ожидайте подтверждения от столовой..."
    )
    await callback.message.answer(user_text, parse_mode="Markdown")

    # Формируем сообщение для админа столовой
    admin_text = (
            f"🔔 **Новый заказ!**\n\n"
            f"🚪 **Комната:** {room}\n"
            f"👤 **Пользователь:** @{callback.from_user.username or 'Без юзернейма'} (ID: {user_id})\n\n"
            f"🥞 **Состав заказа:**\n" + "\n".join(order_details) + f"\n\n"
                                                                   f"💰 **Сумма:** {total_price} руб."
    )

    # Отправляем заказ админу, если его ID настроен
    if ADMIN_ID:
        try:
            admin_markup = get_order_management_keyboard(user_id)
            await bot.send_message(
                chat_id=int(ADMIN_ID),
                text=admin_text,
                reply_markup=admin_markup,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"Не удалось отправить уведомление админу: {e}")

    # Очищаем корзину и убираем анимацию загрузки кнопки
    user_carts[user_id] = []
    await callback.answer()