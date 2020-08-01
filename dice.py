
import random
import time

from common import bot, namedict


prevtime = 0
dropcount = 0

async def handler(event):
    randint = str(random.randint(1,6)) #此处可以准备一个算法。
    uid = str(event['sender']['user_id'])
    alias = event.sender['card']
    if alias == "" : alias = event.sender['nickname']
    alias = namedict.get(uid, alias + ' ')
    #gid = str(event['group_id'])
    now = round(time.time())
    global prevtime
    global dropcount
    if ((now - prevtime) < 3):
        dropcount = dropcount + 1
    else:
        #out = str(now) + ' ' + str(prevtime) + '\n'
        prevtime = now
        out = alias + "抽到了" + randint
        if(dropcount != 0): out = out + '\n' + str(dropcount) + " 个请求因过于频繁被抛弃"
        dropcount = 0
        await bot.send(event, out)

    return
