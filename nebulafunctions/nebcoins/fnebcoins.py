from threading import Thread
import firebase_admin
from firebase_admin import credentials, db
# from firebase_admin import credentials, initialize_app, storage

storagepassword = ''

def init_storage():
    cred = credentials.Certificate("storage/nebcoinstorageSecret.json")
    firebase_admin.initialize_app(cred, {'databaseURL':'https://nebcoinstorage-default-rtdb.firebaseio.com'})
    global ref
    ref = db.reference("/")
    # global storage
    # # cred = credentials.Certificate("static/auth-firebase.json")
    # # initialize_app(cred, {'storageBucket': 'storied-scarab-353711.appspot.com'})
    # # global bucket
    # # bucket = storage.bucket()
    # storage = os.getenv('STORAGE')

def uploaddata(data):
    # blob = bucket.blob('data')
    # blob.upload_from_string(f'{data}')
    # data = {'data': json.dumps(data)}
    # requests.post(f'https://nebstore.onrender.com/{storage}/upload', data=data)
    for i in data.keys():
        time = []
        for t in data[i]['time']:
            if t == None:
                time.append('None')
            else:
                time.append(t)
        data[i]['time'] = time
        for j in data[i].keys():
            if data[i][j] == []:
                data[i][j] = ['empty']
    Thread(target=ref.set, args=(data,)).start()

def getdata():
    # blob = bucket.blob('data.json')
    # # print(dir(blob))
    # # print(blob.open().read())
    # # print()
    # my_json = str(blob.download_as_text().decode('utf8')).replace("'", '"').replace("None", "null")
    # print(my_json)
    # return json.loads(my_json)
    # data = requests.get(f'https://nebstore.onrender.com/{storage}/get').text
    # data = json.loads(data)
    # return data
    data = ref.get()
    for i in data.keys():
        time = []
        for t in data[i]['time']:
            if t == 'None':
                time.append(None)
            else:
                time.append(t)
        data[i]['time'] = time
        for j in data[i].keys():
            if data[i][j] == ['empty']:
                data[i][j] = []
    return data
            

def startf(id):
    try:
        id = str(id)
        data = getdata()
        data[id] = {"farm":[':brown_square::brown_square::brown_square::brown_square:', ':brown_square::brown_square::brown_square::brown_square:', ':brown_square::brown_square::brown_square::brown_square:'], "time":[None,None,None], "bal":100, "inv":[], "pets":[], "level":1, "quests":["Plant Kiwi", "Reach 2000 <:nebcoin:936570857684336640>"]}
        uploaddata(data)
        return "true"
    except:
        return "false"

def getinv(id):    
    try:
        id = str(id)
        try:
            inv = getdata()[id]["inv"]
            return inv
        except:
            return "false"   
    except:
        return None 

def updateinv(id, inv):
    id = str(id)
    try:
        data = getdata()
        data[id]["inv"] = inv
        uploaddata(data)
    except:
        pass

def getmoney(id):
    id = str(id)    
    try:
        id = str(id)
        bal = getdata()[id]["bal"]
        if bal == "false":
            return None
        else:
            return int(bal)
    except:
        return None

def getlevel(id):  
    id = str(id)  
    try:
        lvl = getdata()[id]["level"]
        if lvl == "false":
            return None
        else:
            return int(lvl)
    except:
        return None

def getquests(id): 
    id = str(id)   
    try:
        quests = getdata()[id]["quests"]
        return quests
    except:
        return None

def updatequests(id, quests):  
    id = str(id)  
    try:
        data = getdata()
        data[id]["quests"] = quests
        uploaddata(data)
    except:
        return None

def getpets(id):    
    id = str(id)
    try:
        pets = getdata()[id]["pets"]
        return pets
    except:
        return []


def getfarm(id):
    id = str(id)
    try:
        farm = getdata()[id]["farm"]
        return farm
    except:
        return []

def gettime(id):
    id = str(id)
    try:
        time = getdata()[id]["time"]
        return time
    except:
        return []

def updatemoney(id, money):
    id = str(id)
    try:
        data = getdata()
        data[id]["bal"] = money
        uploaddata(data)
    except:
        pass

def updatelevel(id, level):
    id = str(id)
    try:
        data = getdata()
        data[id]["level"] = level
        uploaddata(data)
    except:
        pass


def updatepets(id, pets):
    id = str(id)
    try:
        data = getdata()
        data[id]["pets"] = pets
        uploaddata(data)
    except:
        pass


def updatefarm(id, farm):
    id = str(id)
    try:
        data = getdata()
        data[id]["farm"] = farm
        uploaddata(data)
    except:
        pass

def updatetime(id, pos, time):
    id = str(id)
    try:
        gtime = gettime(id)
        stime = []
        # if pos == 0:
        #     time = [time, gtime[1], gtime[2]]
        # elif pos == 1:
        #     time = [time, gtime[1], gtime[2]]
        # elif pos == 2:
        #     time = [time, gtime[1], gtime[2]]
        for i in range(len(gtime)):
            if pos == i:
                stime.append(time)
            else:
                stime.append(gtime[i])   
        data = getdata()
        data[id]["time"] = stime
        uploaddata(data)
    except:
        pass

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)

def getplanteddata(userid):
    id = str(userid)
    data = getdata()
    try:
        #BAL
        bal = data[id]["bal"]
        if bal == "false":
            bal = None
        else:
            bal = int(bal)
        #LEVEL
        lvl = data[id]["level"]
        if lvl == "false":
            lvl = None
        #FARM
        farm = data[id]["farm"] 

        return bal, int(lvl), farm
    except:
        return [], None, None

def getinventorydata(userid):
    id = str(userid)
    data = getdata()
    try:
        #BAL
        bal = data[id]["bal"]
        if bal == "false":
            bal = None
        else:
            bal = int(bal)
        #INV
        inv = data[id]["inv"]  
        return bal, inv
    except:
        return None, "false"

def getworkdata(userid):
    id = str(userid)
    data = getdata()
    try:
        #BAL
        bal = data[id]["bal"]
        if bal == "false":
            bal = None
        else:
            bal = int(bal)
        #PETS
        pets = data[id]["pets"]  
        return bal, pets
    except:
        return None, []

def getjourneydata(userid):
    id = str(userid)
    data = getdata()
    try:
        #BAL
        bal = data[id]["bal"]
        if bal == "false":
            bal = None
        else:
            bal = int(bal)
        #PETS
        pets = data[id]["pets"]  
        return bal, pets
    except:
        return None, []

def getleveldata(userid):
    id = str(userid)
    data = getdata()
    try:
        #BAL
        bal = data[id]["bal"]
        if bal == "false":
            bal = None
        else:
            bal = int(bal)
        #QUESTS
        quests = data[id]["quests"]
        #LEVEL
        lvl = data[id]["level"]
        if lvl == "false":
            level = None
        else:
            level = int(lvl)
        #FARM
        farm = data[id]["farm"]
        #TIME
        time = data[id]['time'] 
        return level, quests, bal, farm, time
    except:
        return None, None, None, None

def gettransferdata(id1, id2):
    id1 = str(id1)  
    id2 = str(id2)  
    data = getdata()
    try:
        bal1 = data[id1]["bal"]
        bal2 = data[id2]["bal"]
        if bal1 == "false":
            bal1 = None
        else:
            bal1 = int(bal1)
        if bal2 == "false":
            bal2 = None
        else:
            bal2 = int(bal2)
        return bal1, bal2
    except:
        return None, None

def getfarmdata(userid):
    id = str(userid)
    data = getdata()
    try:
        #BAL
        bal = data[id]["bal"]
        if bal == "false":
            bal = None
        else:
            bal = int(bal)
        #TIME
        time = data[id]['time']
        #FARM
        farm = data[id]["farm"] 
        #INV
        inv = data[id]["inv"]
        return bal, time, farm, inv
    except:
        return None, [], None, "false"


def updateplanted(userid, farm, money, pos, time):
    id = str(userid)
    try:
        #FARM
        data = getdata()
        data[id]["farm"] = farm
        #MONEY
        data[id]["bal"] = money
        #TIME
        gtime = gettime(id)
        stime = []
        # if pos == 0:
        #     time = [time, gtime[1], gtime[2]]
        # elif pos == 1:
        #     time = [time, gtime[1], gtime[2]]
        # elif pos == 2:
        #     time = [time, gtime[1], gtime[2]]
        for i in range(len(gtime)):
            if pos == i:
                stime.append(time)
            else:
                stime.append(gtime[i])   
        data[id]["time"] = stime
        uploaddata(data)
    except:
        pass

def updatesell(userid, inv, money):
    id = str(userid)
    try:
        data = getdata()
        #MONEY
        data[id]["bal"] = money
        #INV
        data[id]['inv'] = inv
        uploaddata(data)
    except:
        pass

def updatejourney(userid, money, pets):
    id = str(userid)
    try:
        data = getdata()
        #MONEY
        data[id]["bal"] = money
        #INV
        data[id]['pets'] = pets
        uploaddata(data)
    except:
        pass

def updatefarmdata(userid, inv, time, farm):
    id = str(userid)
    try:
        data = getdata()
        #INV
        data[id]["inv"] = inv
        #TIME
        data[id]["time"] = time
        #FARM
        data[id]["farm"] = farm
        uploaddata(data)
    except:
        pass

def updateleveldata(userid, farm, level, time):
    id = str(userid)
    try:
        data = getdata()
        #FARM
        data[id]["farm"] = farm
        #LEVEL
        data[id]['level'] = level
        #TIME
        data[id]['time'] = time
        uploaddata(data)
    except:
        pass


# def setfarmminenil():
#     data = getdata()
#     data["811893594716766210"]["farm"] = [':brown_square::brown_square::brown_square::brown_square:', ':brown_square::brown_square::brown_square::brown_square:', ':brown_square::brown_square::brown_square::brown_square:']
#     data["811893594716766210"]["time"] = [None,None,None]
#     print(data)
#     uploaddata(data)

init_storage()
# print(gettime('811893594716766210'))
# updatetime('811893594716766210', 0, '2023-09-22 09:52:53.887006')
# updatetime('811893594716766210', 1, '2023-09-22 09:52:53.887006')
# updatetime('811893594716766210', 2, '2023-09-22 09:52:53.887006')
# updatetime('811893594716766210', 3, '2023-09-22 09:52:53.887006')
# updatepets('811893594716766210', [])
# updatelevel('811893594716766210', 1)
# updateinv('865535420825600031', [])
# setfarmminenil()
