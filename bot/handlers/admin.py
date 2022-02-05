from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb

ID = None

class FSMAdmin(StatesGroup):
	photo = State()
	name = State()
	description = State()
	price = State()

class FSMAdmin1(StatesGroup):
	message_text = State()

#@dp.message_handler(commands=['moderator'], is_chat_admin = True)
async def make_changes_command(message: types.Message):
	global ID 
	ID = message.from_user.id 
	await bot.send_message(message.from_user.id, 'Доступ разрешен', reply_markup=admin_kb.button_case_admin)
	

#начало диалога
#@dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message : types.Message):
	if message.from_user.id == ID:
		await FSMAdmin.photo.set()
		await message.reply('Загрузи фото')


#удаляем элемент по названию
async def cm_delete(message : types.Message):
	if message.from_user.id == ID:
		await FSMAdmin1.message_text.set()
		await message.reply('Введи название')


#выход из состояния
#@dp.message_handler(state="*", commands = 'Отмена')
#@dp.message_handler(Text(equals='Отмена',ignore_case=True),state="*")
async def cancel_handler(message : types.Message, state:FSMContext):
	if message.from_user.id == ID:
		current_state = await state.get_state()
		if current_state is None:
			return
		await state.finish()
		await message.reply('OK')


#ловим ответ
#@dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message : types.Message, state:FSMContext):
	if message.from_user.id == ID:
		async with state.proxy() as data:
			data['photo'] = message.photo[0].file_id
		await FSMAdmin.next()
		await message.reply('Введи название')

#ловим второй ответ
#@dp.message_handler(state=FSMAdmin.name)
async def load_name(message : types.Message, state:FSMContext):
	if message.from_user.id == ID:
		async with state.proxy() as data:
			data['name'] = message.text
		await FSMAdmin.next()
		await message.reply('Введи количество')


#ловим третий ответ
#@dp.message_handler(state=FSMAdmin.description)
async def load_description(message : types.Message, state:FSMContext):
	if message.from_user.id == ID:
		async with state.proxy() as data:
			data['description'] = message.text
		await FSMAdmin.next()
		await message.reply('Укажи цену')

#ловим последний ответ
#@dp.message_handler(state=FSMAdmin.price)
async def load_price(message : types.Message, state:FSMContext):
	if message.from_user.id == ID:
		async with state.proxy() as data:
			data['price'] = float(message.text)
		await sqlite_db.sql_add_command(state)
		await state.finish()
		await message.reply('Успешно')

async def delete_item(message : types.Message, state:FSMContext):
	if message.from_user.id == ID:
		async with state.proxy() as data:
			data['message_text'] = message.text
		await sqlite_db.sql_delete(state)
		await state.finish()
		await message.reply('Успешно')

#посмотреть меню
async def pizza_menu_command(message : types.Message):
	await sqlite_db.sql_read(message)



	

def register_handlers_admin(dp : Dispatcher):
	dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
	dp.register_message_handler(cancel_handler, state="*", commands = ['Отмена'])
	dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
	dp.register_message_handler(load_name, state=FSMAdmin.name)
	dp.register_message_handler(load_description, state=FSMAdmin.description)
	dp.register_message_handler(load_price, state=FSMAdmin.price)
	dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin = True)
	dp.register_message_handler(cm_delete, commands=['Удалить'], state=None)
	dp.register_message_handler(delete_item, state=FSMAdmin1.message_text)
	dp.register_message_handler(pizza_menu_command, commands=['Меню'])




