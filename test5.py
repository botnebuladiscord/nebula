import requests
import json
import os

storage = os.getenv('STORAGE')
data = {'data': '{"811893594716766210": {"farm": [":apple::apple::apple::apple:", ":apple::apple::apple::apple:", ":banana::banana::banana::banana:"], "time": ["2023-09-13 16:42:51.924063", "2023-10-13 16:42:56.461648", "2023-10-13 16:48:00.355126"], "bal": 506, "inv": [":apple:", ":brown_square:", ":brown_square:", ":apple:", ":apple:", ":apple:", ":apple:", ":apple:", ":apple:", ":brown_square:", ":apple:", ":brown_square:", ":brown_square:", ":apple:", ":apple:", ":brown_square:", ":brown_square:"], "pets": [], "level": 2, "quests": ["Plant Kiwi", "Reach 2000 <:nebcoin:936570857684336640>"]}, "865535420825600031": {"farm": [":apple::apple::apple::apple:", ":apple::apple::apple::apple:", ":apple::apple::apple::apple:"], "time": ["2022-09-21 15:08:08.043460", "2022-09-21 15:08:47.946120", "2022-09-21 15:08:52.137617"], "bal": 100, "inv": [], "pets": [], "level": 1, "quests": ["Plant Kiwi", "Reach 2000 <:nebcoin:936570857684336640>"]}, "870612783614558219": {"farm": [":apple::apple::apple::apple:", ":apple::apple::apple::apple:", ":apple::apple::apple::apple:"], "time": [null, "2022-09-07 12:09:43.534611", "2022-09-07 12:10:18.070009"], "bal": 1487, "inv": [], "pets": [], "level": 1, "quests": ["Plant Kiwi", "Reach 2000 <:nebcoin:936570857684336640>"]}}'}
requests.post(f'https://nebcoinstore.isroisthebest.repl.co/{storage}/upload', data=data)

data = requests.get(f'https://nebcoinstore.isroisthebest.repl.co/{storage}/get').text
data = json.loads(data)
print(data['811893594716766210'])