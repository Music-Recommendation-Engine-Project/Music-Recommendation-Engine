import streamlit as st
import os
import requests
import spotipy
import requests
import spotipy.util as util
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
        3. The Login page will redirect you to Spotify Login Page.
        4. Follow the instructions.
        5. Type the name of your favorite artits.
        6. The system will provide 5 Recommended Artist and top songs for each of them.
           The default recommendation model is our [internal] engine. 
           However, if we can't find your artist, we will use [Spotify] model. 
           The name of the model will provided after you type the artist.
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
        
def find_similar_artists_spotify(artist_name, num_artists=5):
    # Search for the artist
    result = sp.search(q='artist:' + artist_name, type='artist')
    items = result['artists']['items']

    if len(items) == 0:
        return []

    # Get the similar artists
    artist_id = items[0]['id']
    related_artists = sp.artist_related_artists(artist_id)['artists']
    return [related_artist['name'] for related_artist in related_artists[:num_artists]]

#Some Styling
st.markdown(
    """
    <style>
    .main-container {
        padding: 3rem;
    }
    .title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .input-container {
        margin-bottom: 2rem;
    }
    .track-container {
        justify-content: space-between;
    }
    .track {
        width: 30%;
        margin-bottom: 2rem;
        border: 1px solid #ddd;
        border-radius: 50px;
        padding: 1rem;
        text-align: center;
    }
    .track-image {
        width: 100%;
        margin-bottom: 1rem;
    }
    .spotify-button {
        background-color: #1DB954;
        color: #fff;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        text-decoration: none;
    }
    widget_style{
            width: 100%;
            height: 100vh;
            border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

#Streamlit App code
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<div class="title">Spotify Artist Search</div>', unsafe_allow_html=True)

# Get user input for artist name
st.markdown('<div class="input-container">', unsafe_allow_html=True)
artist_name = st.text_input("Enter artist name:")
num_items=6
artist_found=False

if artist_name:
    url = f"https://artist-api2023.herokuapp.com/find_similar_artists?artist={artist_name}&num_items={num_items}"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": os.environ["DETA_API"]
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        similar_artists = response.json()
        st.write('Author Found! Using [internal] engine to recommend artists...')
    else:
        st.write('No author found! Using [Spotify] engine to recommend artists....')
        similar_artists = find_similar_artists_spotify(artist_name, num_items)

    st.markdown('</div>', unsafe_allow_html=True)
    artist_found=True
else:
    st.write("Waiting for your artist's name...")
    artist_found=False
    
if artist_found:
    for artist_name in similar_artists[1:]:
        if artist_name:
            # Search for artist
            results = sp.search(q='artist:' + artist_name, type='artist')
            items = results['artists']['items']

            if len(items) > 0:
                # Get top tracks of artist
                artist_id = items[0]['id']
                top_tracks = sp.artist_top_tracks(artist_id)

                # Output top tracks
                with st.container():
                    st.markdown('<div class="track-container">', unsafe_allow_html=True)
                    st.write('Author: ', artist_name)
                    i = 0
                    for track in top_tracks['tracks']:
                        if i <= 5:
                            i += 1
                            track_info = track
                            track_name = track_info['name']
                            track_uri = track_info['uri']
                            track_image_url = track_info['album']['images'][0]['url']
                            preview_url = track_info['preview_url']

                            with st.container():
                                if preview_url is not None:
                                    # Get the Spotify player widget using the Spotify URI
                                    spotify_widget_uri = f"https://open.spotify.com/embed/track/{track_uri.split(':')[-1]}"

                                    # Create the iframe element with the Spotify player widget
                                    spotify_player_html = f"""
                                        <iframe src="{spotify_widget_uri}" width="100%" height="80%" frameborder="0" allowtransparency="true" allow="encrypted-media" style="min-width: 250px; max-width: 440px;"></iframe>
                                    """

                                    # Display the Spotify player widget in your Streamlit app
                                    html(spotify_player_html)
                                else:
                                    st.write('No preview available')
                        st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.write("No similar artists found.")
