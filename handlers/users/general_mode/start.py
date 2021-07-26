from filters import IsPrivate
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, db


@dp.message_handler(CommandStart(deep_link=None), IsPrivate())
async def bot_start(message: types.Message):
    await message.answer(
        "\n".join(
            [
                f'Привет, <b>{message.from_user.full_name}</b>!',
                f'Ты был(а) занесен(а) в базу.',
                f'/help - справка по командам inline режима,\n'
                f'/common_help - справка по командам обычного режима,\n'
                f'/diary_help - справка по командам дневника.'
            ]))
