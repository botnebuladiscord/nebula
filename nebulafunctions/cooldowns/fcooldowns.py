import json
from datetime import datetime, timedelta

def add_cooldown(command, user_id, time):
    user_id = str(user_id)
    with open('storage/cooldowns.json') as file:
        data = json.load(file)
    try:
        data[command]
    except:
        data[command] = {}
    time = datetime.now() + timedelta(seconds=time)
    time = round(time.timestamp())
    data[command][user_id] = time
    with open('storage/cooldowns.json', 'w') as file:
        json.dump(data, file)

def check_cooldown(command, user_id):
    user_id = str(user_id)
    try:
        with open('storage/cooldowns.json') as file:
            data = json.load(file)
        time = data[command][user_id]
        if datetime.fromtimestamp(time) <= datetime.now():
            delete_cooldown(command, user_id)
            return None
        return time
    except:
        return None

def delete_cooldown(command, user_id):
    try:
        user_id = str(user_id)
        with open('storage/cooldowns.json') as file:
            data = json.load(file)
        data[command].pop(user_id)
        with open('storage/cooldowns.json', 'w') as file:
            json.dump(data, file)
    except:
        pass