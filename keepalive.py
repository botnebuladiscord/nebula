from flask import Flask
from threading import Thread
import json

app = Flask('')

@app.route('/')
def home():
    return "Hello. I am alive!"

@app.route('/data')
def data():
    with open('storage/poll.json') as file:
        return json.load(file)

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
