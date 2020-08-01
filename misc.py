
from aiocqhttp import message
from common import *

# 复读机
async def echo(event):
	raw = event.message.replace("echo", "", 1).strip()
	outmsg = message.unescape(raw)
	await bot.send(event, outmsg)

# 复读为CQ码
async def print(event):
	raw = event.message.replace("print", "", 1).strip()
	outmsg = message.escape(raw)
	await bot.send(event, outmsg)