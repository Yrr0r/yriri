
"""
Memo tool:
SYNOPSIS
Use this applet to write your memo and call them out with predefined keywords.
USAGE
memosave [KEY] [VALUE] : store VALUE into KEY
memodelete [KEY] : delete value stored in KEY
Use =[KEY] to call out a value.
**And squre brackets are not part of the command.
"""

from common import *

from sqlconn import db, keepAlive
import pymysql

# Database Procedures

def preserve(keyword, gid, uid, message):
	"preserve(关键词，群号码，发信人，消息内容) \n Returns 0 if insertion fails(Duplicate), or 1 on success."
	# Keepalive
	db.ping(reconnect=True)

	key = gid + "." + keyword

	sqlcmd = " INSERT IGNORE INTO `phrases` (`keyname`, `groupid`, `userid`, `content`, `lastcall`) VALUES (%s, %s, %s, %s, now()); "
	args = [key, gid, uid, message]

	cursor = db.cursor(pymysql.cursors.DictCursor)
	cursor.execute(sqlcmd, args)
	result = cursor.rowcount
	return result


def seek(keyword, gid):
	"seek(关键字，群号), \n Returns the string of message or None if does not exist."
	# Keepalive
	db.ping(reconnect=True)

	key = gid + "." + keyword

	sqlcmd = "SELECT `content` FROM `phrases` WHERE `keyname` = %s"
	args = [key]

	cursor = db.cursor(pymysql.cursors.DictCursor)
	cursor.execute(sqlcmd, args)
	rownums = cursor.rowcount
	if(rownums == 0): return None
	result = cursor.fetchone()

	updatecmd = "UPDATE `phrases` SET `callcount`=`callcount`+ 1 , `lastcall`=now() WHERE `keyname` = %s "
	cursor = db.cursor(pymysql.cursors.DictCursor)
	cursor.execute(updatecmd, args)

	return result['content']

def delete(keyword, gid):
	# Keepalive
	db.ping(reconnect=True)

	key = gid + "." + keyword

	sqlcmd = "DELETE FROM `phrases` WHERE `keyname` = %s"
	args = [key]
	cursor = db.cursor(pymysql.cursors.DictCursor)
	cursor.execute(sqlcmd, args)
	rownums = cursor.rowcount
	if(rownums == 0): return 0
	else: return 1

def whois(keyword, gid):
	# Keepalive
	db.ping(reconnect=True)

	key = gid + "." + keyword
	sqlcmd = "SELECT `userid` FROM `phrases` WHERE `keyname` = %s"
	args = [key]
	cursor = db.cursor(pymysql.cursors.DictCursor)
	cursor.execute(sqlcmd, args)
	if(cursor.rowcount == 0): return None
	dbout = cursor.fetchone()
	return dbout[0]

# Actual procedure
async def generalhandler(event):
	gid = str(event['group_id'])
	uid = str(event.sender['user_id'])
	message = event.message.replace("ph", "", 1).strip()

	if(message.startswith("memosave")):
		rawpair = message.replace("memosave", "", 1).strip()
		pair = rawpair.split(" ", 1)
		if(len(pair) < 2): 
			await bot.send(event, "语法错误 / Syntax Error")
			return
		keyword = pair[0]
		content = pair[1]

		if(keyword == "on-welcome"): # 欢迎语句保护
			if(isAdm(event) == False):
				await bot.send(event, "禁止修改：\nUnauthorized")
				return
		
		if (preserve(keyword, gid, uid, content) == 0 ):
			await bot.send(event, "Your command has safely failed to ensure it is not misinterpreted.\nIf you have a duplicate entry in the record you should probably consider update or delete it first. ")
		else:
			await bot.send(event, keyword + " -> " + content)

	elif(message.startswith("memodelete")):
		keyname = message.replace("memodelete", "", 1).strip()
		if(keyname == ""):
			await bot.send(event, "Please provide exactly one name.")
			return
		if(isAdm(event)):
			if(delete(keyname, gid) == 0):
				await bot.send(event, "Deletion failed, did this key exist?")
				return
			else: await bot.send(event, keyname + " Deleted.")
			return
		owner = whois(keyname, gid)
		if(owner == uid):
			if(delete(keyname, gid) == 0):
				await bot.send(event, "Deletion failed, did this key exist?")
				return
			else: await bot.send(event, keyname + " Deleted")
		else:
			await bot.send(event, "Do not modify someone else's stuff unless you are admin.")


	elif(message.startswith("=")):
		lookup = message.replace("=", "", 1).strip()
		result = seek(lookup, gid)
		if(result == None):
			await bot.send(event, "Key Error: 未登记该语句")
		else:
			await bot.send(event, result)

async def welcomehandler(event):
	gid = str(event['group_id'])
	msg = seek("on-welcome", gid)
	if(msg == None):
		await bot.send(event, "自动欢迎新人")
		return
	elif(msg == "#stopwelcome#"):
		return
	else:
		await bot.send(event, msg)
