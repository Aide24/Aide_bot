from aiogram import types
from loader import dp


#  хэндлер для обработки сообщения без команды
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def bot_echo(message: types.Message):
    bot_user = await dp.bot.get_me()
    name_bot = bot_user.username
    text = f"Здравствуй <b>{message.from_user.full_name}</b>!\nВ боте {name_bot} нет команды на " \
           f"<code>{message.text}</code>.\nУзнать возможности бота можно командами /help, /common_help."
    await message.answer(text)

    # chat_id = message.from_user.id
    # text = f"Пользователь {message.from_user.full_name} написал {message.text}"
    # await dp.bot.send_message(chat_id=chat_id, text=text)
