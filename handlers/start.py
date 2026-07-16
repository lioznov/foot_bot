from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database.db import get_menu, get_user_room, register_user

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