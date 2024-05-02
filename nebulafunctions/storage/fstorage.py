from threading import Thread
import firebase_admin
from firebase_admin import credentials, db
# from firebase_admin import credentials, initialize_app, storage

def init_storage():
    cred = credentials.Certificate("storage/nebcoinstorageSecret.json")
    firebase_admin.initialize_app(cred, {'databaseURL':'https://nebcoinstorage-default-rtdb.firebaseio.com'})
    global ref
    ref = db.reference("/")

def uploaddata(data):
    for i in data.keys():
        if i == 'poll':
            continue
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
    data = ref.get()
    for i in data.keys():
        if i == 'poll':
            continue
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


def uploaddata_poll(data):
    data2 = getdata()
    for i in data.keys():
        try:
            if data[i]['voted'] == []:
                data[i]['voted'] = ['empty']
        except:
            pass
    data2['poll'] = data
    uploaddata(data2)

def getdata_poll():
    data = ref.get()['poll']
    for i in data.keys():
        try:
            if data[i]['voted'] == ['empty']:
                data[i]['voted'] = []
        except:
            pass
    return data
