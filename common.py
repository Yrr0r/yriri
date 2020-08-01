from aiocqhttp import CQHttp, Event
# 最重要的全局变量：机器人本身的对象
bot = CQHttp(api_root='http://127.0.0.1:5700')

#全局变量
global namedict # 昵称服务
namedict = {}

global nickdict # 用户名记忆
nickdict = {}

# Functions:
def getName(uid):
    if(type(uid) is str):
        if(uid in namedict.keys()):
            return namedict[uid]
        else:
            return nickdict[uid]
    if(type(uid) is list):
        result = []
        k = namedict.keys()
        for n in uid:
            if(n in k):
                result.append(namedict[n])
            else:
                result.append(nickdict[n])
        return result

def putlist(arr, idx = False):
    out = ""
    for i, n in enumerate(arr):
        if(idx == False):
            out = out + n + "\n"
        else:
            out = out + str(i+1) + "  " + n + "\n"
    return out[0:-1]

def isAdm(Event):
    role = Event.sender['role']
    if(str(Event.sender['user_id']) == '2435621458'):
        return True
    elif( role == 'admin' or role == 'owner'):
        return True
    else:
        return False


