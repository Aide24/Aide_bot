from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, CommandStart
from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from keyboards.default import user_keyboard
from loader import dp, db


#  хэндлер обработки команды для добавления почты
@dp.message_handler(Command("mail"))
async def update_email(message: types.Message, state: FSMContext):
    await message.answer("Пришли мне свою почту, на которую я могу отправлять файлы и уведомления.",
                         reply_markup=user_keyboard.keyboard)
    await state.set_state("mail")


#  добавление почты в БД
@dp.message_handler(state="mail")
async def enter_email(message: types.Message, state: FSMContext):
    mail = message.text

    import re
    if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", mail):
        db.update_user_email(email=mail, id=message.from_user.id)
        await message.answer(f"Почта занесена в ваши данные.", reply_markup=ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.reply(text=f"Почта указана не верно. Попробуйте еще раз.",
                            reply_markup=user_keyboard.keyboard)


#  хэндлер обработки команды для добавления номера группы
@dp.message_handler(CommandStart(deep_link="number_party"))
@dp.message_handler(Command("party"))
async def update_email(message: types.Message, state: FSMContext):
    await message.answer("Пришли мне свою группу", reply_markup=user_keyboard.keyboard)
    await state.set_state("number_party")


#  добавление номера группы в БД
@dp.message_handler(state="number_party")
async def enter_email(message: types.Message, state: FSMContext):
    number_party = message.text
    if number_party in ['101', '102', '103', '104', '105']:
        db.update_number_party(number_party=number_party, id=message.from_user.id)
        user = db.select_user(id=message.from_user.id)
        await message.answer(f"Данные обновлены. Запись в БД: {user}", reply_markup=ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.reply(text=f"Такой группы не существует, укажи группу еще раз или нажми кнопку отмена",
                            reply_markup=user_keyboard.keyboard)
