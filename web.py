from flask import Flask
from threading import Thread
import datetime

app = Flask('')

@app.route('/')
def home():
    now = datetime.datetime.now()
    return (f'webserver accessed @ {now.strftime("%H:%M %m/%d/%Y")}')

def run():
  app.run(host='0.0.0.0',port=8080)

def persist():
    t = Thread(target=run)
    t.start()