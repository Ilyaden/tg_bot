import sqlite3 as sq 
from create_bot import bot

def sql_start():
	global base, cur
	base = sq.connect('pizza.db')
	cur = base.cursor()
	if base:
		print("Data base connected")
	base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
	base.commit()

async def sql_add_command(state):
	async with state.proxy() as data:
		cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
		base.commit() 

async def sql_read(message):
	for ret in cur.execute('SELECT * FROM menu').fetchall():
		await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nКоличество:\n{ret[2]}\nЦена:\n{ret[-1]}')


async def sql_delete(state):
	async with state.proxy() as data:
		cur.execute('DELETE FROM menu WHERE name = ?',  tuple(data.values()))
		base.commit()   