
from common import *

from sqlconn import db, keepAlive
import pymysql

import pickle

class Admin:
    '权限管理模块'
    # Feature administration
    featlist = ['alias', 'party', 'rolldice', 'memo', 'logging', 'echo']
    defaultperms = ['alias', 'party', 'rolldice']
    perms = {}
    inited = 0

    # DB Procedures:
    def save(self):
        db.ping(reconnect=True) # Keepalive
        dump = pickle.dumps(Admin.perms)
        sqlcmd = """INSERT INTO `config` (`item`, `value`) VALUES ('adm.perms', %s) 
        ON DUPLICATE KEY UPDATE `value`=%s"""
        args = [dump, dump]
        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sqlcmd, args)
        result = cursor.rowcount
        return result
    def load(self):
        db.ping(reconnect=True) # Keepalive
        sqlcmd = """SELECT `value` FROM `config` WHERE `item` = 'adm.perms'; """
        cursor = db.cursor()
        cursor.execute(sqlcmd)
        if(cursor.rowcount == 1):
            result = cursor.fetchone()
            dump = result[0]
            undump = pickle.loads(dump)
            return undump
        else:
            return {}

    def enable(self, gid, feat):
        if(feat in Admin.featlist):
            if(gid not in Admin.perms.keys()): Admin.perms[gid] = []
            Admin.perms[gid].append(feat)
            Admin().save() # 保存配置
            return "已启用" + feat
        return "语法错误或不存在"
    def disable(self, gid, feat):
        if(gid not in Admin.perms.keys()):
            Admin.perms[gid] = []
            return "权限未初始化"
        else:
            Admin.perms[gid].remove(feat)
            Admin().save() # 保存配置
            return "已关闭" + feat
    def isenabled(self, gid, feat):
        if(gid not in Admin.perms.keys()): 
            return False
        if(feat in Admin.perms[gid]):
            return True
    def resetDefault(self, gid): # mkdefault
        Admin.perms[gid] = Admin.defaultperms[:]
        Admin().save() # 保存配置
        return True
    def getCurrPerms(self, gid): # showperms
        if(gid not in Admin.perms.keys()):
            return False
        return Admin.perms[gid]

# Init from DB
Admin.perms =  Admin().load()

async def handler(event):
    if(event.message.startswith("adm")):
        # 更新备用昵称
        uid = str(event.sender['user_id'])
        gid = str(event['group_id'])
        #
        cmdstrs = event.message.split(' ')
        # [0]'adm' [1]cmd [2]param
        if(len(cmdstrs) < 2): return
        cmd = cmdstrs[1]
        if(len(cmdstrs) > 2):feat = cmdstrs[2]
        if((cmd == 'enable') and (uid == '2435621458')):
            result = Admin().enable(gid, feat)
            await bot.send(event, "Adm: " + result)
            return
        if((cmd == 'disable') and isAdm(event)):
            result = Admin().disable(gid, feat)
            await bot.send(event, "Adm: " + result)
            return
        if((cmd == 'mkdefault') and uid == '2435621458'):
            Admin().resetDefault(gid)
            result = "Adm: 已应用默认设置 "
            await bot.send(event, result)
            return
        if((cmd == 'list') and isAdm(event)):
            perms = Admin().getCurrPerms(gid)
            if(perms == False):
                result = "未初始化权限"
            else:
                result = "当前权限列表：\n"
                result = putlist(perms)
            await bot.send(event, result)
            return
