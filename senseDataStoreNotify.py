import os
import sqlite3 as sqlite
import time
import requests
from sense_emu import SenseHat

def pushNotifications():
	API_KEY = 'o.dca8wKmxpLiAokfc1hC1220Uw316iHhB'
	IDEN = 'ujBpGly0Kf6sjAbxZrFbC8'

	resp = requests.get('https://api.pushbullet.com/v2/devices', auth=(API_KEY, ''))
	print(resp.json())
	data = {
	'type':'note',
	'title':'Take A jacket with you its less than 20C',
	'body':'I can send push notifications now to my phone',
	'device_iden' : IDEN
	}

	resp = requests.post('https://api.pushbullet.com/api/pushes', data=data, auth=(API_KEY, ''))

from datetime import datetime

sense = SenseHat()
sense.clear()

humidity = sense.get_humidity()
temp = sense.get_temperature()

if temp < 21:
	pushNotifications()

cTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

rows = [( cTime, temp, humidity )]

DATABASE = "./sensehat.db"
conn = sqlite.connect(DATABASE)
cur = conn.cursor()
cur.executemany('insert into sensedata values (?,?,?)', rows)
conn.commit()


