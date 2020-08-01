
import pymysql

dbserver = 'localhost'
dbuser = 'qqbot'
dbpasswd = 'qqbot'
dbname = 'qqbot'

db = pymysql.connect(dbserver,dbuser,dbpasswd,dbname)

def keepAlive():
    try:
        db.ping(reconnect=True)
    except:
        db = pymysql.connect(dbserver,dbuser,dbpasswd,dbname)
    return db
