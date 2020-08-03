
"""
SYNOPSIS
一起傻嗨！
USAGE
party [功能] [参数]
功能：
join - 加入游戏 (no args)
leave - 离开 (no args)
pool - 看看列表里有谁 (no args)
kick[ID] - 踢人，ID写QQ号 (Admin only)
玩法：
shuffle - 返回一个打乱的列表
"""
from common import *

import numpy

global party # 群P用户组
party = {}
global lastrock # 上次活动的时间
lastrock = 0

APPLET = 'party'
PREFIX = ''

async def handler(event):
	cmdname = PREFIX + APPLET
	if(event.message.startswith(cmdname) ):
		cmd = event.message.replace(cmdname, "", 1).strip()
		uid = str(event.sender['user_id'])
		gid = str(event['group_id'])
		if(gid not in party.keys()): party[gid] = []
		partylist = party[gid]
		if(cmd == 'join'):
			if(uid not in partylist): partylist.append(uid)
			await bot.send(event, getName(uid) + "加入派对\n" + putlist(getName(partylist)) + "\n ^")
		elif(cmd == 'leave'):
			if(uid in partylist): 
				partylist.remove(uid)
				await bot.send(event, getName(uid) + "已离开")
		elif(cmd == 'pool'):
			if(len(partylist) == 0):
				await bot.send(event, "现在没人在玩")
			else:
				await bot.send(event, putlist(getName(partylist)))
		elif(cmd.startswith('kick')):
			if(event.sender['role'] == 'admin' or event.sender['role'] == 'owner' or uid == "2435621458"):
				kickid = cmd.replace('kick','',1).strip()
				if(kickid in partylist):
					partylist.remove(kickid)
					await bot.send(event, "已删除。剩余玩家: \n" + putlist(getName(partylist)))
				else:
					await bot.send(event, "列表中已经没有这个ID")

		elif(cmd == 'shuffle'):
			shuffled = numpy.random.permutation(partylist).tolist()
			await bot.send(event, "本轮结果\n" + putlist(getName(shuffled), True))
