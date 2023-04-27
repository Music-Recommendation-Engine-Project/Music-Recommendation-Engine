import streamlit as st
import os
import requests
import spotipy
import requests
import spotipy.util as util
from find_similar import find_similar_artists
from streamlit.components.v1 import html
from spotipy.oauth2 import SpotifyOAuth

# Initialize the Web Playback SDK
from IPython.display import display, Javascript
from urllib.parse import quote

#Set environment for Spotify API
client_id = os.environ["SPOTIFY_CLIENT_ID"]
client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]
redirect_uri = 'https://song-recommender2023.herokuapp.com/'
scope = 'user-read-playback-state,user-modify-playback-state,user-read-private'

# Set page configuration — must be the first line of any Streamlit app.
st.set_page_config(
    page_title="Spotify Artist Search",
    page_icon=":musical_note:",
    layout="wide"
)

# Initialize Spotipy
sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
#token_info = []#sp_oauth.get_cached_token()

st.title('Spotify Recommender System')
st.subheader("How it works: \n")
st.write(""" 
        1. Click Login button below to Log into our Spotify.
        2. You may skip the first step but you won't be able to play music.
        3. The Login page will redirect you.
        4. Copy the URL of the redirected page.
        5. Type the name of your favorite artits.
        6. The system will provide 4 Recommended Artist and top songs for each of them.
        7. Play Music and Enjoy!\n\n
        """)

auth_url = sp_oauth.get_authorize_url()
st.markdown(f"<a href='{auth_url}' target='_blank'>Log in with Spotify</a>", unsafe_allow_html=True)
response_url = st.text_input("Enter the URL you were redirected to:")
code = sp_oauth.parse_response_code(response_url)
token_info = sp_oauth.get_access_token(code)

access_token = token_info['access_token']
sp = spotipy.Spotify(auth=access_token)

#Helper Functions
def init_spotify_player(access_token):
    display(Javascript("""
        require(['https://sdk.scdn.co/spotify-player.js'], function(spotify) {
            window.Spotify = spotify;
            window.Spotify.Player.create({
                name: 'Streamlit Player',
                getOAuthToken: function(cb) { cb('""" + access_token + """'); }
            }).connect();
        });
    """))

init_spotify_player(access_token)

def play_track(access_token, track_uri):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = f"https://api.spotify.com/v1/tracks/{track_uri.split(':')[-1]}"
    response = requests.get(url, headers=headers)
    track_info = response.json()

    if response.status_code == 200 and 'preview_url' in track_info and track_info['preview_url']:
        preview_url = track_info['preview_url']
        st.write("Successfully started playing the track.")
        st.audio(preview_url)
    else:
        st.write(f"Failed to start playing the track. Status code: {response.status_code}")


#Streamlit App code
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<div class="title">Spotify Artist Search</div>', unsafe_allow_html=True)

# Get user input for artist name
st.markdown('<div class="input-container">', unsafe_allow_html=True)
artist_name = st.text_input("Enter artist name:")
num_items=6
