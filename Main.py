#!/usr/bin/env python3
# coding=utf-8

from aiocqhttp import CQHttp, Event

from common import *

import adm
from adm import Admin

import dice
import alias
import party
import memo
import chatlog
import misc

def gethelp(ask):
	askable = ['alias', 'party']
	if(ask in askable):
		return (eval(ask).__doc__).strip()
	else:
		return "手册里查不到这个喵"

@bot.on_message("group")
async def _(event: Event):
	message = event.message
	
	gid = str(event['group_id'])
	uid = str(event.sender['user_id'])

	# 更新备用昵称列表
	nickdict[uid] = str(event.sender['nickname'])

	# Adm
	if(event.message.startswith("adm")):
		await adm.handler(event)
	
	# Help
	if(event.message.startswith("help") or event.message.startswith("man")):
		await bot.send(event, gethelp(event.message.replace("help",'',1).strip()))
	
	# Nicks
	if(message.startswith("alias")):
		await alias.handler(event)
	# Dice
	elif(message == "rolldice" and Admin().isenabled(gid, 'rolldice')):
		await dice.handler(event)
	# Party
	elif(message.startswith("party") and (Admin().isenabled(gid, 'party'))):
		await party.handler(event)

	# 复读机
	elif(message.startswith("echo") and (Admin().isenabled(gid, "echo"))):
		await misc.echo(event)
	# 倒复读
	elif (message.startswith("print") and (Admin().isenabled(gid, "echo"))):
		await misc.print(event)

	# saving a memo
	elif(message.startswith("memo") and (Admin().isenabled(gid, 'memo'))):
		await memo.generalhandler(event)

	# call a memo
	if(message.startswith("=") and (Admin().isenabled(gid, 'memo'))):
		await memo.generalhandler(event)

# 日志工具
@bot.on_message("group")
async def _(event: Event):
	gid = str(event['group_id'])
	if(Admin().isenabled(gid, 'logging')):
		await chatlog.logger(event)


# 欢迎新人，在memo中处理
@bot.on_notice('group_increase') #等价于 @bot.on('notice.group_increase')
async def handle_group_increase(event: Event):
	await memo.welcomehandler(event)

# Web
app = bot.server_app

@app.route('/')
async def webroot():
	return ''' <h1> Wrong place, Wrong time. </h1> '''

# run web server
bot.run(host='172.17.0.1', port=9090)
