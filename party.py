
from common import *

import numpy

global party # 群P用户组
party = {}
global lastrock # 上次活动的时间
lastrock = 0

async def handler(event):
    if(event.message.startswith("party") ):
        cmd = event.message.replace("party", "", 1).strip()
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
