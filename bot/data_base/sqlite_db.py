import sqlite3 as sq 
from create_bot import bot


def sql_start():
	global base, cur
	base = sq.connect('shop.db')
	cur = base.cursor()
	if base:
		print("data base 'shop.db' connected")
	base.execute('CREATE TABLE IF NOT EXISTS menu(name TEXT PRIMARY KEY, description TEXT , number_ TEXT, price TEXT)')
	base.commit()

async def sql_add_command(state):
	async with state.proxy() as data:
		cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
		base.commit() 

async def sql_read(message):
	for ret in cur.execute('SELECT * FROM menu').fetchall():
		await bot.send_message(message.from_user.id,  f'--{ret[0]} {ret[1]}:\n   {ret[2]} шт [{ret[3]} р/шт]')

async def sql_read2():
	return cur.execute('SELECT * FROM menu').fetchall()


async def sql_read_number_(number_):
	for number_ in cur.execute('SELECT number_ FROM menu WHERE name = ?', (number_,)).fetchall():
		return (f'{number_[0]}')
	


async def sql_delete(data):
	cur.execute('DELETE FROM menu WHERE name == ?',  (data,))
	base.commit()   


async def sql_change(state):
	async with state.proxy() as data:
		item = list(data.values())
		cur.execute('UPDATE menu SET number_ = ? WHERE name = ?', (item[1], item[0]))
		base.commit()  



	


