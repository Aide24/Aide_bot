from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, CommandStart, RegexpCommandsFilter, Text
from keyboards.inline.status_keyboard import keyboard_with_status
from loader import dp, bot, db, scheduler
from keyboards.default import user_keyboard, list_keyboard
from data.config import admins
import pytz
import re


# async def migraine_record(dp: Dispatcher, id, state: FSMContext):
async def migraine_record(dp: Dispatcher, id):
    # text = f"Введи запись в журнал мигрени."
    # await dp.bot.send_message(chat_id=id, text=text)
    # await state.set_state("record")
    await dp.bot.send_message(chat_id=id, text=f"Оцени свое состояние сегодня", reply_markup=keyboard_with_status())


async def schedule_jobs(id, state):
    user = db.select_user(id=id)

    time = user[4]
    print(time)
    hour = int(f'{time[0]}{time[1]}')
    print(hour)
    minute = int(f'{time[3]}{time[4]}')
    print(minute)

    if user[5] is not None:
        scheduler.remove_job(job_id=user[5])

    job = scheduler.add_job(migraine_record, 'cron', day_of_week='mon-sun', hour=hour, minute=minute,
                            timezone=pytz.timezone('Europe/Moscow'),
                            args=(dp, id))
    # args = (dp, id, state))
    db.update_user_id_job(id_job=job.id, id=id)
    print(scheduler.print_jobs())


@dp.message_handler(Command("set_time"))
async def update_email(message: types.Message, state: FSMContext):
    user = db.select_user(id=message.from_user.id)

    if user[4] is None:
        await message.answer("Введите время в формате ЧЧ:ММ по Москве.", reply_markup=user_keyboard.keyboard)
        await state.set_state("set_time")
    else:
        await message.answer(f"Твое предыдущее время {user[4]}. Введите новое время в формате ЧЧ:ММ по Москве.",
                             reply_markup=user_keyboard.keyboard)
        await state.set_state("set_time")


@dp.message_handler(state="set_time")
async def enter_time(message: types.Message, state: FSMContext):
    time = message.text
    if re.match(r'[0-2]?[0-9]{1}[.:-]{1}[0-9]{2}', time) and len(time) <= 5:
        if len(time) == 4:
            time = '0' + time
        print(time)
        db.update_user_time(time=time, id=message.from_user.id)
        user = db.select_user(id=message.from_user.id)

        if message.from_user.id in admins:
            await message.answer(f"Данные обновлены. Запись в БД: {user}", reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer(f"Данные обновлены. Ваше время {user[4]}.", reply_markup=ReplyKeyboardRemove())
        await state.finish()
        await schedule_jobs(message.from_user.id, state)
    else:
        await message.reply(text=f"Некорректный ввод времени. Попробуйте еще раз.",
                            reply_markup=user_keyboard.keyboard)


@dp.message_handler(Text(contains="Нет", ignore_case=True), state="break_records")
async def confirm_entry_no(message: types.Message, state: FSMContext):
    await message.answer(f"Хорошо, удачного дня.", reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(Text(contains="Да", ignore_case=True), state="break_records")
async def confirm_entry_yes(message: types.Message, state: FSMContext):
    user = db.select_user(id=message.from_user.id)
    if user[5] is not None:
        try:
            scheduler.remove_job(job_id=user[5])
        except Exception as e:
            print(e)
        await message.answer(f"Бот больше не будет тебя спрашивать о состоянии дня.",
                             reply_markup=ReplyKeyboardRemove())
        await state.finish()
    else:
        await state.finish()
        await message.answer(f"Бот не спрашивает тебя о состоянии дня.",
                             reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Command("break_records"))
async def update_email(message: types.Message, state: FSMContext):
    await message.answer("Ты хочешь, чтобы бот не спрашивал тебя о состоянии дня?",
                         reply_markup=list_keyboard.general_keyboard)
    await state.set_state("break_records")
