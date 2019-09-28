from flask import Flask, render_template, flash, request, redirect

import os
import json
import requests
from bs4 import BeautifulSoup as Soup
import spotipy.util as util
import spotipy
import spotipy.oauth2 as oauth2
from dateutil.parser import parse
import datetime

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
port = int(os.environ.get('PORT', 8888))

client_id = 'CLIENT_ID'
client_secret = 'CLIENT_SECRET'
redirect_uri = 'http://localhost:8888/callback'

scope = 'user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played user-top-read playlist-modify-public'

SONGKICK_API_KEY = 'SONGKICK_API_KEY'

artists = []
gig_dates = []
gig_uris = []
tracks = []
tracks_name = []
tracks_image = []

location = ''
min_date = ''
max_date = ''

CITY = ''

curr_artist = 100
curr_round = 100
ready = True

player_url = "https://api.spotify.com/v1/me/player"

prev_url = ''

credentials = oauth2.SpotifyClientCredentials(client_id = "CLIENT_ID", client_secret = "CLIENT_SECRET")
token = credentials.get_access_token()
sp = spotipy.Spotify(auth=token)

@app.route("/callback", methods=['GET'])
def callback():
    global sp
    credentials = spotipy.oauth2.SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        state=None,
        cache_path=None,
        proxies=None)

    code = request.args.get('code')
    global token
    token = credentials.get_access_token(code)
    token = token['access_token']

    return 'ok'

@app.route("/play", methods=['GET'])
def play():
    print("PLAAY")
    print(curr_artist)
    print(len(tracks))
    artist_index = curr_artist % len(tracks)
    update_player(artist_index)
    info = get_info_artist(artist_index)
    return info

@app.route("/pause", methods=['GET'])
def pause():
    print("PAUSEE")
    return 'pause'

@app.route("/previous", methods=['GET'])
def previous():
    global curr_artist
    curr_artist -= 1
    artist_index = (curr_artist) % len(tracks)
    update_player(artist_index)
    info = get_info_artist(artist_index)
    return info

@app.route("/next", methods=['GET'])
def next():
    global curr_artist
    curr_artist += 1
    artist_index = (curr_artist) % len(tracks)
    update_player(artist_index)
    info = get_info_artist(artist_index)
    return info

@app.route("/create_playlist", methods=['GET'])
def create_playlist():
    return 'create playlist'

@app.route("/kiwi_detected", methods=['GET'])
def kiwi_detected():
    print('kiwi_detected')
    url = request.args.get('url')
    url = url.split('/')

    global location
    global min_date
    global max_date

    global ready
    global prev_url

    global artists
    global gig_dates
    global gig_uris
    global tracks
    global tracks_name
    global tracks_image

    if is_date(url[-1]) == True and is_date(url[-2]) == True and url[-3] != '-' and ready == True and url != prev_url:
        ready == False
        artists = []
        gig_dates = []
        gig_uris = []
        tracks = []
        tracks_name = []
        tracks_image = []
        
        max_date = url[-1]
        min_date = url[-2]
        location = url[-3]
        print(location,min_date,max_date)
        get_tracks()

        artist_index = curr_artist % len(tracks)
        update_player(artist_index)
        info = get_info_artist(artist_index)
        ready = True
        prev_url = url
        return info
    else:
        return 'kiwi_detected'

def get_info_artist(artist_index):
    info = str(artists[artist_index])+'$'+str(tracks_name[artist_index][0])+'$'+str(tracks_image[artist_index][0])+'$'+str(gig_dates[artist_index])+'$'+str(gig_uris[artist_index])+'$'+str(CITY)
    return info

def is_date(string, fuzzy=False):
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

def get_artists(LOCATION, MIN_DATE, MAX_DATE):
    LOCATION = LOCATION.split('-')
    global CITY
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
            date = concert['start']['date']
            date = datetime.datetime.strptime(date, "%Y-%m-%d")
            gig_dates.append(datetime.date.strftime(date, "%d %B"))
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

def get_tracks():
    print('Getting tracks...')
    get_artists(location, min_date, max_date)

    artists_id = []
    global token
    sp = spotipy.Spotify(auth=token)

    for artist in artists:
        top_tracks = []
        top_tracks_names = []
        top_tracks_images = []
        artist_searched = sp.search(artist, limit=10, offset=0, type='artist', market=None)
        artist_id = artist_searched['artists']['items'][0]['id']
        artists_id.append(artist_id)
        for track in sp.artist_top_tracks(artist_id)['tracks']:
            print('track:',track)
            track_id = track['uri']
            track_name = track['name']
            track_image = track['album']['images'][1]['url']
            top_tracks.append(track_id)
            top_tracks_names.append(track_name)
            top_tracks_images.append(track_image)
            print(track_id)
        tracks.append(top_tracks)
        tracks_name.append(top_tracks_names)
        tracks_image.append(top_tracks_images)

    print(tracks)
    print(tracks_name)
    print(tracks_image)

    artist_index = curr_artist % len(tracks)
    update_player(artist_index)

def update_player(artist_index):
    authorization = {'Authorization': 'Bearer ' + token}
    params = {'uris': [tracks[artist_index][0]]}
    response = requests.put(player_url + '/play', headers=authorization, data=json.dumps(params))
    print('playback:',response.content)

@app.route("/", methods=['GET', 'POST'])
def hello():
    print('at hello')
    return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)