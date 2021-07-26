from loader import dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram import types
from aiogram.types import ReplyKeyboardRemove


@dp.message_handler(Text(contains="Отмена", ignore_case=True) | Command(commands=['break']))
@dp.message_handler(Text(contains="Отмена", ignore_case=True) | Command(commands=['break']),
                    state=["number_party", "set_time", "break_records", "record", "mail"])
async def break_state(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply(text="Произведена отмена ввода. Кнопки клавиатуры удалены. Состояние обновлено.",
                        reply_markup=ReplyKeyboardRemove())
