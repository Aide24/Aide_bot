from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


# Кастомный фильтр на Приватный чат с ботом
class IsPrivate(BoundFilter):

    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE
