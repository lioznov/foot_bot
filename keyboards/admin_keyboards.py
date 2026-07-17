from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_order_management_keyboard(user_id:int)->InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Принять заказ ✅", callback_data=f"accept_order_{user_id}"),
            InlineKeyboardButton(text="Отклонить заках ❌",callback_data=f"reject_order_{user_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)