from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db
from data_base import makeorder_db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

ID = None

class FSMClient(StatesGroup):
	name = State()
	number_ = State()
	id_ = State()



#@dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
	await bot.send_message(message.from_user.id, "добро пожаловать", reply_markup=kb_client)

		
#@dp.message_handler(commands=['Меню'])
async def product_command(message : types.Message):
	await sqlite_db.sql_read(message)


#добавление первого товара в корзину
async def cm_buy(message : types.Message):
	
	read = await sqlite_db.sql_read2()
	for ret in read:
		await bot.send_message(message.from_user.id, f'--{ret[0]} {ret[1]}:\n   {ret[2]} шт [{ret[3]} р/шт]', reply_markup=InlineKeyboardMarkup().\
			add(InlineKeyboardButton(f'добавить в заказ {ret[0]}', callback_data=f'add {ret[0]}')))
	await FSMClient.name.set()

#отмена
async def cancel_handler(message : types.Message, state:FSMContext):
	current_state = await state.get_state()
	if current_state is None:
		return
	await state.finish()
	await message.reply('ok')



async def add_name(callback_query: types.CallbackQuery, state:FSMContext):
	item = callback_query.data.replace('add ', '')
	async with state.proxy() as data:
		data['name'] = item
	await FSMClient.next()
	await callback_query.answer(text='укажите количество', show_alert=True)


async def add_number_(message : types.Message, state:FSMContext):
	async with state.proxy() as data:
		number1 = int(await sqlite_db.sql_read_number_(data['name']))
		try:
			data['number_'] = int((message.text))
			if ((int(data['number_']) > int(number1)) or (int(data['number_'])<=0) ):
				await message.answer('в наличии нет такого количества, введите число меньше')
				return

			if (int(data['number_']) <= int(number1) and (int(data['number_'])>0)):
				await FSMClient.next()
				await message.answer('хотите добавить еще товар?')
			

		except ValueError:
			await message.answer('введи число')

	
async def add_id(message : types.Message, state:FSMContext):
	global ID 
	ID = message.from_user.id
	async with state.proxy() as data:
		data['id_'] = ID
	

	if (message.text == 'да'):
		await makeorder_db.sql_add_command(state)
		await state.finish()
		await cm_buy(message)
		
		
	if (message.text == 'нет'):
		await makeorder_db.sql_add_command(state)
		await message.reply('заказ создан')
		await state.finish()







def register_handlers_client(dp : Dispatcher):
	dp.register_message_handler(cancel_handler, state="*", text = 'отмена')


	dp.register_message_handler(command_start, commands=['start', 'help'])
	dp.register_message_handler(product_command, text='в наличии')
	dp.register_message_handler(product_command, commands=['stock'])

	dp.register_message_handler(cm_buy, text='купить')
	dp.register_callback_query_handler(add_name,  lambda x: x.data and x.data.startswith('add '), state=FSMClient.name)
	dp.register_message_handler(add_number_, state=FSMClient.number_)
	dp.register_message_handler(add_id, state=FSMClient.id_)
	
	
		
