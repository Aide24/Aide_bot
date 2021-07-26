from filters import IsPrivate
from data.config import admins
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, db


@dp.message_handler(CommandStart(deep_link=None), IsPrivate(), user_id=admins)
async def bot_start(message: types.Message):

    count = db.count_users()[0]

    await message.answer(
        "\n".join(
            [
                f'Привет, {message.from_user.full_name}!\n',
                f'Ты являешься администратором этого бота.\n',
                f'В базе <b>{count}</b> пользователей бота.\n'
                f'/info - команда информации для администратора.',
            ]))
