import os
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from functools import wraps
from random import choice
import time

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(64)
app.config["SESSION_COOKIE_NAME"] = "spotify-auth-session"
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True


# Load the environment variables
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")
scope = os.getenv("SCOPE")

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Set Authorization Manager
auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, 
                            scope=scope, cache_path=".spotifycache", show_dialog=True)

"""ROUTES"""

@app.route('/login')
def login():
    auth_url = auth_manager.get_authorize_url()
    return render_template("login.html", auth_url=auth_url)


@app.route('/callback')
def callback():
    if request.args.get("code"):
        # Being redirected from Spotify auth page
        token_info = auth_manager.get_access_token(request.args.get("code"), check_cache=False)
        session["spotify_token"] = token_info["access_token"]
        session["spotify_token_expiry"] = token_info["expires_in"] + time.time()
        session["spotify_refresh_token"] = token_info["refresh_token"]

        return redirect('/')
    
    flash("Error when logging in")
    return redirect('/login')


@app.route('/log_out')
def log_out():
    session.clear()
    return redirect('/login')


# Function to request user authentication and validate/update token
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Token validation
        if "spotify_token" not in session:
            return redirect('/login')
        # Check if the access token has expired and update
        token_expiry = session.get('spotify_token_expiry')
        if token_expiry != None and token_expiry < time.time():
            refresh_token = session.get('spotify_refresh_token')
            new_token_info = auth_manager.refresh_access_token(refresh_token)
            session['spotify_token'] = new_token_info['access_token']
            session['spotify_token_expiry'] = new_token_info['expires_in'] + time.time()
        
        return f(*args, **kwargs)
    return decorated


@app.route('/user_informations')
@requires_auth
def user_informations():
    # Spotipy library tool
    sp = Spotify(auth_manager=auth_manager)

    username = sp.me()['display_name']
    user_picture = sp.me()['images'][0]['url']

    return jsonify(username=username, user_picture=user_picture)


@app.route('/')
@requires_auth
def index():
    return render_template("index.html")


@app.route('/artists')
@requires_auth
def artists():
    # Spotipy library tool
    sp = Spotify(auth_manager=auth_manager)
    
    # Gets the user's top 10 favorite/most listened artists (uri)
    favorite_artists = sp.current_user_top_artists(limit=10)['items']
    artists_uri = set()
    for artist in favorite_artists:
        uri = artist['uri']
        artists_uri.add(uri)

    # Get artists similar to one of the user's favorite artists
    artists_related = sp.artist_related_artists(choice(tuple(artists_uri)))['artists']
    
    # Select an artist to recommend
    random_artist = choice(artists_related)
    artist_id = random_artist['id']

    return render_template('artists.html', artist_id=artist_id)

# Route to retrieve new artists without needing to refresh the page 
@app.route('/get_new_artist', methods=['GET'])
@requires_auth
def get_new_artist():
    # Spotipy library tool
    sp = Spotify(auth_manager=auth_manager)
    
    # Gets the user's top 10 favorite/most listened artists (uri)
    favorite_artists = sp.current_user_top_artists(limit=10)['items']
    artists_uri = set()
    for artist in favorite_artists:
        uri = artist['uri']
        artists_uri.add(uri)

    # Get artists similar to one of the user's favorite artists
    artists_related = sp.artist_related_artists(choice(tuple(artists_uri)))['artists']
    
    # Select an artist to recommend
    random_artist = choice(artists_related)
    artist_id = random_artist['id']

    return jsonify(artist_id=artist_id)


@app.route('/songs')
@requires_auth
def songs_recommendation():
    # Spotipy library tool
    sp = Spotify(auth_manager=auth_manager)

    # Gets the user's top 10 favorite/most listened artists (uri)
    favorite_artists = sp.current_user_top_artists(limit=5)['items']
    artists_id = [artist['id'] for artist in favorite_artists]

    # Creates a playlist for the user
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user_id, 'Recommendations by SoundExplorer', public=True, description='recommendation playlist by SoundExplorer')
    playlist_id = playlist['id']

    # # Get a list of recommended tracks
    recommended_tracks = sp.recommendations(seed_artists=artists_id, limit=100)['tracks']
    tracks_id = [track['id'] for track in recommended_tracks]

    sp.playlist_add_items(playlist_id, tracks_id)

    return render_template('songs.html', playlist_id=playlist_id)

@app.route('/get_new_playlist')
def get_new_playlist():
    # Spotipy library tool
    sp = Spotify(auth_manager=auth_manager)

    # Gets the user's top 5 favorite/most listened artists (uri)
    favorite_artists = sp.current_user_top_artists(limit=5)['items']
    artists_id = [artist['id'] for artist in favorite_artists]

    # Creates a playlist for the user
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user_id, 'Recommendations by SoundExplorer', public=True, description='recommendation playlist by SoundExplorer')
    playlist_id = playlist['id']

    # # Get a list of recommended tracks
    recommended_tracks = sp.recommendations(seed_artists=artists_id, limit=100)['tracks']
    tracks_id = [track['id'] for track in recommended_tracks]

    sp.playlist_add_items(playlist_id, tracks_id)

    return jsonify(playlist_id=playlist_id)


@app.route('/top_tracks')
@requires_auth
def top_tracks():
    # Spotipy library tool
    sp = Spotify(auth_manager=auth_manager)

    # Gets user country
    country = sp.me()['country']

    # Search for the official Spotify playlist with the most played songs in the user's country.
    results = sp.search(q='Top', type='playlist', limit=1, market=country)

    # Gets the playlist id 
    playlist_id = results['playlists']['items'][0]['id']
    

    return render_template('top_tracks.html', playlist_id=playlist_id)
    
    
if __name__ == "__main__":
    app.run(debug=True)




