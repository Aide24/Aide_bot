from aiogram import types
from filters import IsPrivate
from loader import dp, db

from data.config import admins


@dp.message_handler(IsPrivate(), text="/info", user_id=admins)
async def admin_chat_secret(message: types.Message):
    info_about_count_user = db.count_users()[0]
    users = db.select_all_users()
    list_users = ", ".join([item[1] for item in users])
    await message.answer("Здравствуй, администратор бота Aide.\n"
                         f"Сейчас ботом пользуются {info_about_count_user} пользователя.\n"
                         f"Список пользователей: <b>{list_users}</b>")

