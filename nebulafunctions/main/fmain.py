import json

def isblacklist(id):
    id = str(id)
    try:
        with open('/storage/blacklist.json') as file:
            data = json.load(file)
        return data[id]["reason"]
    except:
        return None