from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Команда старта"),
        types.BotCommand("common_help", "Команда помощи в обычном режиме"),
        types.BotCommand("help", "Команда помощи в inline режиме"),
        types.BotCommand("diary_help", "Команда помощи в режиме дневника"),
        types.BotCommand("mail", "Указать свою почту"),
        types.BotCommand("party", "Указать свою группу"),
        types.BotCommand("break", "Удалить все состояния и кнопки"),
        types.BotCommand("articles", "Вывести статьи по ботам"),
        types.BotCommand("set_time", "Указать время задования вопроса состояния"),
        types.BotCommand("send", "Отослать дневник состояния на почту"),
        types.BotCommand("break_records", "Отмена задавания вопроса ботом"),
    ])
