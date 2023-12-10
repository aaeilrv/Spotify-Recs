from datetime import datetime
import requests
from flask import Flask, jsonify, redirect, request, session, send_file
import urllib.parse as urlparse
from dotenv import load_dotenv
import json
import os

app = Flask(__name__)
app.secret_key = 'secret_key'

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:3000/callback'
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

@app.route('/')
def index():
    scope = "user-read-private user-read-email user-library-read"

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True
    }
    
    auth_url = f'{AUTH_URL}?{urlparse.urlencode(params)}'

    return redirect(auth_url)

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({'error': request.args['error']})
    
    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()

        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

        return redirect('/tracks')
    
@app.route('/tracks')
def tracks():
    if 'access_token' not in session:
        return redirect('/')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    ### TRACKS ###
    limit = 50
    iter = 0
    track_jsons = []
    songs_id = []
    songs_name = []
    songs_artist = []

    while True:
        # Obtén las canciones de la biblioteca del usuario en lotes de 50 (límite de API)
        response = requests.get(f'{API_BASE_URL}me/tracks/?offset={iter * 50}&limit={limit}', headers=headers)

        for item in response.json()['items']:
            track_id = item['track']['id']
            track_name = item['track']['name']
            track_artist = item['track']['artists'][0]['name']
            track_album = item['track']['album']['name']
            track_popularity = item['track']['popularity']
            track_duration = item['track']['duration_ms']
            track_explicit = item['track']['explicit']
            track_url = item['track']['external_urls']['spotify']

            track_info_json = {
                'id': track_id,
                'name': track_name,
                'artist': track_artist,
                'album': track_album,
                'popularity': track_popularity,
                'duration': track_duration,
                'explicit': track_explicit,
                'url': track_url
            }

            track_jsons.append(track_info_json)
            songs_id.append(track_id)
            songs_name.append(track_name)
            songs_artist.append(track_artist)
        
        if response.json()['next'] == None:
            break

        iter += 1

    ### AUDIO FEATURES ###

    batch_size = 100
    track_features_jsons = []

    # Obtén las características de audio de las canciones en lotes de 100 (límite de API)
    for i in range(0, len(songs_id), batch_size):
        batch_ids = songs_id[i:i + batch_size]
        songs_id_str = ','.join(batch_ids)
        request_url = f'{API_BASE_URL}audio-features/?ids={songs_id_str}'

        response = requests.get(request_url, headers=headers)    

        if response.status_code == 200:
            for item in response.json()['audio_features']:
                track_id = item['id']
                track_name = songs_name[songs_id.index(track_id)]
                track_artist = songs_artist[songs_id.index(track_id)]
                track_danceability = item['danceability']
                track_energy = item['energy']
                track_key = item['key']
                track_loudness = item['loudness']
                track_mode = item['mode']
                track_speechiness = item['speechiness']
                track_acousticness = item['acousticness']
                track_instrumentalness = item['instrumentalness']
                track_liveness = item['liveness']
                track_valence = item['valence']
                track_tempo = item['tempo']
                track_time_signature = item['time_signature']

                track_features_json = {
                    'id': track_id,
                    'name': track_name,
                    'artist': track_artist,
                    'danceability': track_danceability,
                    'energy': track_energy,
                    'key': track_key,
                    'loudness': track_loudness,
                    'mode': track_mode,
                    'speechiness': track_speechiness,
                    'acousticness': track_acousticness,
                    'instrumentalness': track_instrumentalness,
                    'liveness': track_liveness,
                    'valence': track_valence,
                    'tempo': track_tempo,
                    'time_signature': track_time_signature
                }

                track_features_jsons.append(track_features_json)
        else:
            print(f"Error for batch {i}-{i+batch_size}: {response.status_code}")
    
    json_filename = 'tracks.json'
    with open(json_filename, 'w') as json_file:
        json.dump(track_features_jsons, json_file)

    return send_file(json_filename, mimetype='application/json', as_attachment=True)


if __name__ == '__main__':
    app.run(port=3000, debug=True)