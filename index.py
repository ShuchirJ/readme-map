from flask import Flask, request
import requests, os
from pysondb import db
from utils import generate_shades

app = Flask(__name__)
db = db.getDb("db.json")

@app.route('/')
def home():
    client_ip = request.remote_addr
    if client_ip == "127.0.0.1": client_ip = "193.122.164.255"
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

    countries = {}
    for loc in locations:
        country = loc['location'].split(", ")[1]
        if country not in countries:
            countries[country] = 0
        countries[country] += loc['value']
    countries = sorted(countries.items(), key=lambda x: x[1], reverse=True)
    countries = [country[0].lower() for country in countries if country[1] > 0]
    print(countries)
    
    shades = generate_shades("#ADD8E6", len(countries))

    svgData = open("worldmap.svg", "r").read()
    for country in countries:
        svgData = svgData.replace(f'id="{country}"', f'id="{country}" fill="{shades[countries.index(country)]}"')
    
    return svgData

app.run(host='0.0.0.0', debug=True)