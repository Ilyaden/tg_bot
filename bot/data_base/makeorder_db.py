import sqlite3 as sq 
from create_bot import bot

def sql_start():
	global base, cur
	base = sq.connect('makeorder.db')
	cur = base.cursor()
	if base:
		print("data base 'makeorder.db' connected")
	base.execute('CREATE TABLE IF NOT EXISTS menu(name TEXT , number_ TEXT, id_ TEXT)')
	base.commit()


async def sql_add_command(state):
	async with state.proxy() as data:
		cur.execute('INSERT INTO menu VALUES (?, ?, ?)', tuple(data.values()))
		base.commit() 