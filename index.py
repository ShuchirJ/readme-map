from flask import Flask, request
import requests, os
from pysondb import db

app = Flask(__name__)
db = db.getDb("db.json")

@app.route('/')
def home():
    client_ip = request.remote_addr
    if client_ip == "127.0.0.1": client_ip = "67.20.255.175"
    r = requests.get(f'http://ip-api.com/json/{client_ip}')
    data = r.json()
    location = f"{data['regionName']}, {data['countryCode']}"
    if db.getBy({"location": location}):
        value = db.getBy({"location": location})[0]['value'] + 1
        db.update({"location": location}, {"value": value})
    else:
        value = 1
        db.add({"location": location, "value": value})

    locations = db.getAll()
    print(locations)
    return 'Hello, World!'

app.run(host='0.0.0.0', debug=True)