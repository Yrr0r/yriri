
from common import *

from sqlconn import db, keepAlive
import pymysql

from aiocqhttp import MessageSegment

# Database Procedures
def savelog(gid, sender, message):
    "Design: 返回0表示存储失败，返回1表示成功"
    # Keepalive
    db.ping(reconnect=True)

    sqlcmd = """ INSERT INTO `chatlog` (`time`, `gid`, `sender`, `message`) VALUES (now(), %s, %s, %s);"""
    args = [gid, sender, message]

    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sqlcmd, args)
    result = cursor.rowcount
    print(str(result))
    return result

class counters:
    failsInARow = 0

async def logger(event):
    #global failsInARow
    gid = str(event['group_id'])
    uid = str(event.sender['user_id'])
    message = str(event.message)

    if(savelog(gid, uid, message) == 0):
        counters.failsInARow = counters.failsInARow + 1
        if(counters.failsInARow < 10):
            await bot.send(event, "你数据库掉线了，快去修 " + MessageSegment.at(2435621458))
        return
    else:
        counters.failsInARow = 0
        return
