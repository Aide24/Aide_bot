from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

general_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                       keyboard=[
                                           [
                                               KeyboardButton(text="Да"), KeyboardButton(text="Нет")
                                           ],
                                           [
                                               KeyboardButton(text="Отмена")
                                           ]
                                       ])

status_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                      keyboard=[
                                          [
                                              KeyboardButton(text="1"), KeyboardButton(text="2")
                                          ],
                                          [
                                              KeyboardButton(text="3"), KeyboardButton(text="4")
                                          ],
                                          [
                                              KeyboardButton(text="5"), KeyboardButton(text="6")
                                          ],
                                          [
                                              KeyboardButton(text="7"), KeyboardButton(text="8")
                                          ],
                                          [
                                              KeyboardButton(text="9"), KeyboardButton(text="10")
                                          ]
                                      ])
