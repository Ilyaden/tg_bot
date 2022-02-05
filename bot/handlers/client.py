from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db

#@dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
	await bot.send_message(message.from_user.id, "Бот работает", reply_markup=kb_client)
		


#@dp.message_handler(commands=['Режим_работы'])
async def pizza_open_command(message : types.Message):
		await bot.send_message(message.from_user.id, "Круглосуточно")


#@dp.message_handler(commands=['Меню'])
async def pizza_menu_command(message : types.Message):
	await sqlite_db.sql_read(message)


def register_handlers_client(dp : Dispatcher):
	dp.register_message_handler(command_start, commands=['start', 'help'])
	dp.register_message_handler(pizza_open_command, commands=['Режим_работы'])
	dp.register_message_handler(pizza_menu_command, commands=['Меню'])
	
		
