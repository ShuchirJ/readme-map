from flask import Flask, request
import requests, os
from pysondb import db
from utils import generate_shades
from bs4 import BeautifulSoup

app = Flask(__name__)
db = db.getDb("db.json")

@app.route('/<username>')
def home(username):

    dark_mode = request.args.get('theme', 'light').lower() == 'dark'

    client_ip = request.remote_addr
    if 'X-Forwarded-For' in request.headers:
        client_ip = request.headers['X-Forwarded-For'].split(',')[0].strip()
    elif 'X-Real-IP' in request.headers:
        client_ip = request.headers['X-Real-IP']
    if client_ip == "127.0.0.1": client_ip = "108.156.11.0"
    r = requests.get(f'http://ip-api.com/json/{client_ip}')
    data = r.json()
    location = f"{data['regionName'] if data['regionName'] else '--'}, {data['countryCode']}"
    if db.getBy({"location": location, "username": username}):
        value = db.getBy({"location": location, "username": username})[0]['value'] + 1
        db.update({"location": location, "username": username}, {"value": value})
    else:
        value = 1
        db.add({"location": location, "username": username, "value": value})

    locations = db.getBy({"username": username})
    locations = sorted(locations, key=lambda x: x['value'], reverse=True)
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

    top5Locations = locations[:5]

    emojis = []
    for country in top5Locations:
        country = country['location'].split(", ")[1]
        chars = list(country_code_to_flag_emoji(country.upper()))
        chars = [str(hex(ord(c)))[2:] for c in chars]
        print(chars)
        emojis.append(f"https://raw.githubusercontent.com/twitter/twemoji/master/assets/svg/{'-'.join(chars)}.svg")
    print(emojis)

    shades = generate_shades("#ADD8E6", len(countries))

    svgData = open("light_template.svg", "r").read() if not dark_mode else open("dark_template.svg", "r").read()
    mapData = open("worldmap.svg", "r").read()
    if dark_mode:
        soup = BeautifulSoup(mapData, "xml")
        for tag in soup.find_all(['g', 'path']):
            if tag.has_attr('id') and len(tag['id']) == 2:
                tag['fill'] = "white"
        mapData = str(soup)

    for country in countries:
        soup = BeautifulSoup(mapData, "xml")
        color = shades[countries.index(country)]
        tag = soup.find(id=country)
        if tag:
            tag['fill'] = color
        mapData = str(soup)

    # Remove XML declaration from mapData if present
    if mapData.startswith('<?xml'):
        mapData = mapData.split('?>', 1)[-1].lstrip()

    svgData = svgData.replace("{{map}}", mapData)
    svgaData = svgData.replace("{{flag1}}", emojis[0] if len(emojis) > 0 else "")
    svgaData = svgaData.replace("{{flag2}}", emojis[1] if len(emojis) > 1 else "")
    svgaData = svgaData.replace("{{flag3}}", emojis[2] if len(emojis) > 2 else "")
    svgaData = svgaData.replace("{{flag4}}", emojis[3] if len(emojis) > 3 else "")
    svgaData = svgaData.replace("{{flag5}}", emojis[4] if len(emojis) > 4 else "")

    svgData = svgaData.replace("{{place1}}", top5Locations[0]['location'] if len(top5Locations) > 0 else "")
    svgData = svgData.replace("{{place2}}", top5Locations[1]['location'] if len(top5Locations) > 1 else "")
    svgData = svgData.replace("{{place3}}", top5Locations[2]['location'] if len(top5Locations) > 2 else "")
    svgData = svgData.replace("{{place4}}", top5Locations[3]['location'] if len(top5Locations) > 3 else "")
    svgData = svgData.replace("{{place5}}", top5Locations[4]['location'] if len(top5Locations) > 4 else "")

    response = app.response_class(svgData, mimetype='image/svg+xml')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
    return response


def country_code_to_flag_emoji(country_code):
    """
    Convert a 2-letter country code to its emoji flag.
    Example: 'US' → '🇺🇸'
    """
    if len(country_code) != 2:
        raise ValueError("Country code must be 2 letters")
    base = 0x1F1E6  # Unicode codepoint for 'REGIONAL INDICATOR SYMBOL LETTER A'
    return ''.join(chr(base + ord(char.upper()) - ord('A')) for char in country_code)


app.run(host='0.0.0.0', debug=True)