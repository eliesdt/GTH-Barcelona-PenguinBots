from flask import Flask, render_template, flash, request, redirect

import os
import json
import requests
from bs4 import BeautifulSoup as Soup

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
#app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'
port = int(os.environ.get('PORT', 8888))

SONGKICK_API_KEY = 'gULl2n89adTbdK7G'

@app.route("/callback", methods=['GET'])
def callback():
    print(request.args.get('code'))
    return 'ok'

#localhost:8888/get_artists?location=france&min_date=2019-10-03&max_date=2019-10-05
@app.route("/get_artists", methods=['GET'])
def get_artists():
    artists = []
    gig_dates = []
    gig_uris = []

    LOCATION = request.args.get('location')
    MIN_DATE = request.args.get('min_date')
    MAX_DATE = request.args.get('max_date')

    LOCATION = LOCATION.split('-')
    CITY = LOCATION[0]
    COUNTRY = LOCATION[-1]

    response = requests.get('http://musicbrainz.org/ws/2/area/?query={}'.format(COUNTRY))
    soup = Soup(response.content,'xml')
    country_code = soup.find('iso-3166-1-code').getText()

    response = requests.get("https://api.songkick.com/api/3.0/search/locations.json?query={}&apikey={}".format(LOCATION,SONGKICK_API_KEY))
    content = response.content
    js = json.loads(content)
    area_id = js['resultsPage']['results']['location'][0]['metroArea']['id']

    response = requests.get(
        'https://api.songkick.com/api/3.0/metro_areas/{}/calendar.json?min_date={}&max_date={}&apikey={}'.format(area_id,MIN_DATE,MAX_DATE,SONGKICK_API_KEY))
    content = response.content
    js = json.loads(content)

    for concert in js['resultsPage']['results']['event']:
        for artist in concert['performance']:
            gig_uris.append(concert['uri'])
            gig_dates.append(concert['start']['date'])
            artists.append(artist['displayName'])

    for i in reversed(range(len(artists))):
        formatted_artist = artists[i].replace(" ","+")

        response = requests.get('https://musicbrainz.org/ws/2/artist/?query={}&fmt=json'.format(formatted_artist))
        content = response.content
        js = json.loads(content)

        try:
            country = js['artists'][0]['country']
            if country != country_code:
                del artists[i]
                del gig_dates[i]
                del gig_uris[i]
        except:
            del artists[i]
            del gig_dates[i]
            del gig_uris[i]

    response = ''
    for i in range(len(artists)):
        response = response + '{} will perfom on {}, more info: {}'.format(artists[i],gig_dates[i],gig_uris[i])

    return f"{response}"

@app.route("/", methods=['GET', 'POST'])
def hello():
    print('at hello')
    return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)