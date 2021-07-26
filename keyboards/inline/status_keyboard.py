from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def keyboard_with_status():
    commodity_field = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [
            InlineKeyboardButton(text="1 🤕", callback_data="Ужасно"),
            InlineKeyboardButton(text="2 🤒", callback_data="Очень плохо"),
            InlineKeyboardButton(text="3 🤧", callback_data="Плохо")
        ],
        [
            InlineKeyboardButton(text="4 😪", callback_data="Удовлетворительно"),
            InlineKeyboardButton(text="5 😓", callback_data="Приемлимо"),
            InlineKeyboardButton(text="6 🥱", callback_data="Нормально")
        ],
        [
            InlineKeyboardButton(text="7 🙂", callback_data="Хорошо"),
            InlineKeyboardButton(text="8 😁", callback_data="Отлично"),
            InlineKeyboardButton(text="9 😎", callback_data="Супер")
        ]
    ])
    return commodity_field
