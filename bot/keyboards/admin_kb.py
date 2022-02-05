from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button_load = KeyboardButton("/Загрузить")
button_delete = KeyboardButton("/Удалить")
button_cancel = KeyboardButton("/Отмена")
button_menu = KeyboardButton("/Меню")


button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_load).add(button_delete).add(button_cancel).add(button_menu)