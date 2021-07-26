from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram import types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from keyboards.inline.status_keyboard import keyboard_with_status
from keyboards.default import list_keyboard
from loader import dp, bot, db

import datetime
import pytz


@dp.callback_query_handler(
    text=["Ужасно", "Очень плохо", "Плохо", "Удовлетворительно", "Приемлимо", "Нормально", "Хорошо", "Отлично",
          "Супер"])
async def query_scheduler(call: types.CallbackQuery, state: FSMContext):
    moscow_time = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    await call.answer(cache_time=60)
    descriptions = db.select_record(id_recording=call.from_user.id, date=moscow_time.date())

    if descriptions:
        await call.message.answer(f"Ты уже указывал состояние сегодня. Твое состояние <b>{descriptions[0][3]}</b>.\n"
                                  f"Удачного дня!")
    else:
        moscow_time = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
        db.add_recording(id_recording=call.from_user.id, date=moscow_time.date(), status=call.data)
        print(db.select_all_recording())
        await call.message.answer(text=f"Твое самочувствие на сегодня {call.data}.\n"
                                       f"Хочешь описать сегодняшний день?", reply_markup=list_keyboard.general_keyboard)
        await state.set_state("record")


@dp.message_handler(Command("record"))
async def start_input(message: types.Message, state: FSMContext):
    await message.answer(f"Оцени свое масочувствие", reply_markup=keyboard_with_status())


@dp.message_handler(Text(contains="Да", ignore_case=True), state="record")
async def confirm_entry_yes(message: types.Message, state: FSMContext):
    await message.answer(f"Введи описание сегодняшнего дня.", reply_markup=ReplyKeyboardRemove())
    await state.set_state("description")


@dp.message_handler(Text(contains="Нет", ignore_case=True), state="record")
async def confirm_entry_no(message: types.Message, state: FSMContext):
    await message.answer(f"Хорошо, удачного дня.", reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(state="description")
async def enter_record(message: types.Message, state: FSMContext):
    moscow_time = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    db.add_description(description=message.text, id_recording=message.from_user.id, date=moscow_time.date())
    await message.answer(f"Хорошо, удачного дня.", reply_markup=ReplyKeyboardRemove())
    print(db.select_all_recording())
    await state.finish()
