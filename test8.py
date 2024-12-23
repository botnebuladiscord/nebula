import requests, json, random
temp = requests.get('https://api.memegen.link/templates').text
temp = json.loads(temp)
print(len(temp))
ii = -1
for i in temp:
    ii += 1
    if len(temp[ii]['example']['text']) > 2:
        print(temp[ii])
        print('\n...\n')
meme = requests.post('https://api.memegen.link/images', data={'template_id':'aag', 'text[]':['foo', 'bar', 'quack']}).text
print(meme)
# meme = json.loads(meme)
# meme = meme['data']['memes']
# meme = random.choice(meme)
# print(meme)