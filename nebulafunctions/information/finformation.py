import wikipediaapi
import json
import requests
import urllib.request
import urllib.parse
from PIL import Image, ImageFont, ImageDraw

def fwikipedia(query):
    query = str(query).replace('what ', '')
    query = str(query).replace('when ', '')
    query = str(query).replace('how ', '')
    query = str(query).replace('which ', '')
    query = str(query).replace('who ', '')
    query = str(query).replace(' a ', '')
    query = str(query).replace(' the ', '')
    query = str(query).replace(' is ', '')
    query = str(query).replace(' are ', '')
    wiki_wiki = wikipediaapi.Wikipedia('nebula', 'en')
    page_py = wiki_wiki.page(query)
    a = page_py.summary
    if a == '':
        return None, None
    title = str(query).split(' ')
    title = ' '.join(title).upper()
    a = a.replace('\n', '\n\n')
    a = a.replace(query, f'**{query}**')
    a = a.replace(query.upper(), f'**{query.upper()}**')
    a = a.replace(query.capitalize(), f'**{query.capitalize()}**')
    a = a + f'\n\nTaken From https://en.wikipedia.org/wiki/{query}'
    return title, a

def fweather(city):
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID=80fdac2a94ecb0f7d25a602e14efc511&units=metric'
        data = json.loads(requests.get(url).content)
        data = data['main']
        temp = data['temp']
        temp_max = data['temp_max']
        temp_min = data['temp_min']
        humidity = data['humidity']
        url = f'http://api.weatherapi.com/v1/current.json?key=9e5b6d5c74a54b01a5361331211612&q={city}&aqi=no'
        data = json.loads(requests.get(url).content)
        wetype = data["current"]["condition"]["icon"]
        wetypet = data["current"]["condition"]["text"]
        wetype = str(wetype).replace('//', '')
        f = open('assets/weather/wetype.png','wb')
        f.write(requests.get(f'http://{wetype}').content)
        f.close()
        wetype = Image.open('assets/weather/wetype.png')

        img = Image.open('assets/weather/wb.jpeg')
        font = ImageFont.truetype('storage/fonts/hf.ttf', 60)
        font2 = ImageFont.truetype('storage/fonts/hf.ttf', 30)
        font3 = ImageFont.truetype('storage/fonts/hf.ttf', 20)
        font4 = ImageFont.truetype('storage/fonts/Roboto-Black.ttf', 10)

        img2 = ImageDraw.Draw(img)

        img2.text((140, 15), 'Weather', fill=(255,255,255), font=font)
        img2.text((20, 100), f'City: {city.capitalize()}', fill=(255,255,255), font=font2)
        img2.text((20, 150), f'Temperature: {temp}°C', fill=(255,255,255), font=font2)
        img2.text((25, 200), f'Minimum: {temp_min}°C', fill=(255,255,255), font=font3)
        img2.text((25, 230), f'Maximum: {temp_max}°C', fill=(255,255,255), font=font3)
        img2.text((25, 260), f'Humidity: {humidity}', fill=(255,255,255), font=font3)
        img2.text((25, 290), f'Condition: {wetypet}', fill=(255,255,255), font=font3)
        img2.text((0, 320), f'Taken From: openweathermap.org and weatherapi.com', fill=(255,255,255), font=font4)

        img.save('assets/weather/weather.png')

        img = Image.open('assets/weather/weather.png')
        img2 = Image.open('assets/weather/logo.png')

        img2 = img2.resize((70,70))

        img.paste(img2, (425, 260), img2)
        img.paste(wetype, (435, 3), wetype)

        img.save('assets/weather/weather.png')
    except Exception as e:
        print(e)
        return 404
    
def get_fact():
  response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").text
  json_data = json.loads(response)
  fact = json_data['text']
  return (fact)

def question(num=None, difficulty=None):
    if num != None and difficulty != None:
        url = f"https://opentdb.com/api.php?amount=1&category={num}&difficulty={difficulty}&encode=url3986"
    elif num != None and difficulty == None:
        url = f"https://opentdb.com/api.php?amount=1&category={num}&encode=url3986"
    elif num == None and difficulty != None:
        url = f"https://opentdb.com/api.php?amount=1&difficulty={difficulty}&encode=url3986"
    else:
        url = "https://opentdb.com/api.php?amount=1&encode=url3986"
    r = requests.get(url)
    json_data = json.loads(r.text)
    qs = json_data['results'][0]['question']
    d = json_data["results"][0]['difficulty']
    incorrect = json_data['results'][0]['incorrect_answers']
    correct = json_data['results'][0]['correct_answer']
    qs = urllib.parse.unquote(qs)
    correct = urllib.parse.unquote(correct)
    incorrect2 = []
    for i in incorrect:
        i = urllib.parse.unquote(i)
        incorrect2.append(i)
    incorrect = incorrect2
    
    return(qs, incorrect, correct, d)