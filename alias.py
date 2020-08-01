# Set the alias.
# Need to fix this in future.

from common import bot, namedict, nickdict

from adm import Admin

async def handler(event):
    gid = str(event['group_id'])
    userid = str(event.sender['user_id'])
    name = event.message.replace("alias", "", 1)
    name = name.strip()
    en = (Admin().isenabled(gid, 'alias'))
    output = ""
    if(name != "" and en ): #如果设置名称非空，且
        namedict[userid] = name #插入/修改字典
        output = "将使用" + name + "称呼" + userid
    elif((name == "") and (userid in namedict.keys()) ): # 设置名称为空，但是有记录
        del(namedict[userid])
        output = userid + "的别名已被删除。"
    elif(en): # 设置名称为空，无记录
        output = userid + "尚未设置别名。"

    if(output != ""):
        await bot.send(event, output)
    return
