import json
from datetime import timedelta, datetime
from nebulafunctions.storage.fstorage import *

def poll(mesid, time, voted, votes, et, a, q, ch, guild):
    data = getdata_poll()
    try:
        data.pop(str(mesid))
        uploaddata_poll(data)
    except:
        pass
    ids = data
    ids[mesid] = {'time': time,'et': et, 'voted':voted, 'votes': votes, 'a':a, 'q':q, 'ch':ch, 'guild':guild}
    uploaddata_poll(ids)

# def getv(mid):
#     try:
#         with open("storage/poll.json") as file:
#             data = json.load(file)
#             jsonData = data[mid]
#             for x in jsonData:
#                 if x == 'voted':
#                     return data[mid]["voted"]    
#     except:
#         return 0 
    
# def getet(mid):
#     try:
#         with open("storage/poll.json") as file:
#             data = json.load(file)
#             jsonData = data[mid]
#             for x in jsonData:
#                 if x == 'et':
#                     return data[mid]["et"]    
#     except:
#         return 0 
    
# def geta(mid):
#     try:
#         with open("storage/poll.json") as file:
#             data = json.load(file)
#             jsonData = data[mid]
#             for x in jsonData:
#                 if x == 'a':
#                     return data[mid]["a"]    
#     except:
#         return 0  
    
# def getch(mid):
#     try:
#         with open("storage/poll.json") as file:
#             data = json.load(file)
#             jsonData = data[mid]
#             for x in jsonData:
#                 if x == 'ch':
#                     return data[mid]["ch"]    
#     except:
#         return 0  
    
# def getq(mid):
#     try:
#         with open("storage/poll.json") as file:
#             data = json.load(file)
#             jsonData = data[mid]
#             for x in jsonData:
#                 if x == 'q':
#                     return data[mid]["q"]    
#     except:
#         return 0       

# def gett(mid):
#     try:
#         with open("storage/poll.json") as file:
#             data = json.load(file)
#             jsonData = data[mid]
#             for x in jsonData:
#                 if x == 'time':
#                     return data[mid]["time"]    
#     except:
#         return 0       

# def getvn(mid):
#     try:
#         with open("storage/poll.json") as file:
#             data = json.load(file)
#             jsonData = data[mid]
#             for x in jsonData:
#                 if x == 'votes':
#                     return data[mid]["votes"]    
#     except:
#         return 0
    
# def getguild(mid):
#     try:
#         with open("storage/poll.json") as file:
#             data = json.load(file)
#             jsonData = data[mid]
#             for x in jsonData:
#                 if x == 'guild':
#                     return data[mid]["guild"]    
#     except:
#         return 0
    
def pollupdatevotedvotes(mid, voted, votes):
    try:
        data = getdata_poll()
        data[mid]["voted"] = voted
        data[mid]["votes"] = votes
        uploaddata_poll(data)
    except:
        pass

def setcomplete(mid):
    try:
        data = getdata_poll()
        data.pop(str(mid))
        data[mid] = 'OVER'
        uploaddata_poll(data)
    except:
        pass
    
# def checkcomplete(mid):
#     try:
#         with open("storage/poll.json") as file:
#             data = json.load(file)
#         return data[str(mid)] == 'OVER'
#     except:
#         return False
    
def convert_time(time):
    pos = ['s', 'm', 'h', 'd']
    time_dict = {'s':1, 'm':60, 'h':3600, 'd':3600*24}
    unit = time[-1]
    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2
    return val * time_dict[unit]
    
def addtempban(userid, time, guildid):
    time = convert_time(time)
    time2 = timedelta(0, time)
    time2 = datetime.now() + time2
    day = time2.strftime('%d')
    year = time2.strftime('%Y')
    month = time2.strftime('%m')
    hour = time2.strftime('%H')
    minute = time2.strftime('%M')
    time = datetime(int(year), int(month), int(day), int(hour), int(minute)).timestamp() 
    time = round(time)
    with open('storage/tempban.json') as file:
        data = json.load(file)
    data[userid] = [time, guildid]
    with open('storage/tempban.json','w') as file:
        json.dump(data, file)

def checktempban(userid):
    with open('storage/tempban.json') as file:
        data = json.load(file)
    return data[userid][0]

def deletetempban(userid):
    with open('storage/tempban.json') as file:
        data = json.load(file)
    data.pop(userid)
    with open('storage/tempban.json','w') as file:
        json.dump(data, file)
        
def gettempbanguild(userid):
    with open('storage/tempban.json') as file:
        data = json.load(file)
    return data[userid][1]

def giveawayf(mesid, time, prize, author, channel, guild):
    with open('storage/giveaway.json') as file:
        data = json.load(file)
    data[str(mesid)] = {"time":time, "prize":prize, "author":author, "channel":channel, "guild":guild}
    with open('storage/giveaway.json', 'w') as file:
        data = json.dump(data, file)

def getgauthor(giveawayid):
    giveawayid = str(giveawayid)
    try:
        with open('storage/giveaway.json') as file:
            data = json.load(file)
        return data[giveawayid]["author"]
    except:
        return None

def getgtime(giveawayid):
    giveawayid = str(giveawayid)
    try:
        with open('storage/giveaway.json') as file:
            data = json.load(file)
        return data[giveawayid]["time"]
    except:
        return None
    
def getgprize(giveawayid):
    giveawayid = str(giveawayid)
    try:
        with open('storage/giveaway.json') as file:
            data = json.load(file)
        return data[giveawayid]["prize"]
    except:
        return None
    
def getgchannel(giveawayid):
    giveawayid = str(giveawayid)
    try:
        with open('storage/giveaway.json') as file:
            data = json.load(file)
        return data[giveawayid]["channel"]
    except:
        return None
    
def getgguild(giveawayid):
    giveawayid = str(giveawayid)
    try:
        with open('storage/giveaway.json') as file:
            data = json.load(file)
        return data[giveawayid]["guild"]
    except:
        return None
    
def addwarn(userid, reason, modid, guildid):
    userid = str(userid)
    guildid = str(guildid)
    try:
        with open('storage/warnings.json') as file:
            data = json.load(file)
        hexuserid = hex(int(userid))
        hexuserid = str(hexuserid).replace('0x', '')
        if guildid not in data.keys():
            data[guildid] = {}
        if userid in data[guildid].keys():
            num = int(data[guildid][userid][-1]['id'][-1]) + 1
            warnid = hexuserid + 'm' + str(modid) + str(num)
            data[guildid][userid].append({'reason':reason, 'id':warnid})
        else:
            num = 1
            warnid = hexuserid + 'm' + str(modid) + str(num)
            data[guildid][userid] = [{'reason':reason, 'id':warnid}]
        with open('storage/warnings.json','w') as file:
            json.dump(data, file)
        return num, warnid
    except:
        return None
    
def getwarns(userid, guildid):
    userid = str(userid)
    guildid = str(guildid)
    try:
        with open('storage/warnings.json') as file:
            data = json.load(file)
        return data[guildid][userid]
    except:
        return None
    
def delwarn(warnid, guildid):
    userid = str(warnid)
    userid = userid.split('m')[0]
    userid = int(userid, 16)
    userid = str(userid)
    guildid = str(guildid)
    try:
        with open('storage/warnings.json') as file:
            data = json.load(file)
        ii = 0
        for i in data[guildid][userid]:
            if i['id'] == warnid:
                data[guildid][userid].pop(ii)
                break
            ii += 1
        with open('storage/warnings.json','w') as file:
            json.dump(data, file)
        return len(data[guildid][userid]), userid
    except:
        return None
