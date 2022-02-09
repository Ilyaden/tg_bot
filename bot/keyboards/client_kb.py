from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



b1 = KeyboardButton('в наличии')
b2 = KeyboardButton('купить')
b3 = KeyboardButton('отмена')



kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.row(b1,b2)
kb_client.add(b3)

