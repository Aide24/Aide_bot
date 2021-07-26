from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, CommandStart, Text
from aiogram import types
from keyboards.default import user_keyboard
from loader import dp, db


#  хэндлер для добавления пользователя через deep_link
@dp.message_handler(CommandStart(deep_link="connect_user"))
async def connect_user(message: types.Message):
    db.add_user(message.from_user.id, message.from_user.full_name)
    await message.answer("Здравствуй! Ты подключен к Aide bot. "
                         "Узнать о возможностях этого бота можно командой /help")


#  хэндлер для обработки deep link для добавления номера группы
@dp.message_handler(CommandStart(deep_link="number_party"))
@dp.message_handler(Command("party"))
async def update_email(message: types.Message, state: FSMContext):
    await message.answer("Пришли мне свою группу", reply_markup=user_keyboard.keyboard)
    await state.set_state("number_party")  # хэндлер для добавления группы находится в database_commands
