import uvicorn
import os
import numpy as np
import pandas as pd
from fastapi import FastAPI
from typing import List
from io import BytesIO, StringIO
from deta import Deta  # Import Deta for storage

# Initialize with a Project Key
project_key = os.environ["DETA_PROJECT_KEY"]
deta = Deta(project_key)

# This how to connect to or create a database.
database_name = os.environ["DETA_DATABASE_NAME"]
drive = deta.Drive(database_name)

def load_embeddings():
    #Lookup table for artists that we can use
    item_lookup_stream = drive.get('item_lookup.csv')
    content = item_lookup_stream.read().decode('utf-8')
    item_lookup = pd.read_csv(StringIO(content), index_col=[0])
    item_lookup_stream.close()

    #Model Factors
    item_factors_stream = drive.get('item_factors.npy')
    #Loading bytes stream
    content_factors = item_factors_stream.read()
    load_factors = BytesIO(content_factors)
    loaded_factors = np.load(load_factors, allow_pickle=True)
    #close bytes stream
    item_factors_stream.close()

    #Models Biases
    item_biases_stream = drive.get('item_biases.npy')
    content_biases = item_biases_stream.read()
    load_bytes_biases = BytesIO(content_biases)
    loaded_biases = np.load(load_bytes_biases, allow_pickle=True)
    item_biases_stream.close()

    return loaded_factors, loaded_biases, item_lookup

def find_similar_artists(artist=None, num_items=10, item_lookup=None, item_factors=None, item_biases=None):
    if item_factors is None or item_biases is None or item_lookup is None:
        item_factors, item_biases, item_lookup = load_embeddings()

    # Get the item id for the given artist
    item_id = int(item_lookup[item_lookup.artist_name == artist]['artist_id'])

    # Get the item vector for our item_id and transpose it.
    item_vec = item_factors[item_id].T

    # Calculate the similarity between the given artist and all other artists
    # by multiplying the item vector with our item_matrix
    scores = np.add(item_factors.dot(item_vec), item_biases).reshape(1, -1)[0]

    # Get the indices for the top num_items scores
    top_indices = np.argsort(scores)[::-1][:num_items]

    # We then use our lookup table to grab the names of these indices
    # and add it along with its score to a pandas dataframe.
    artists, artist_scores = [], []

    for idx in top_indices:
        artists.append(
            item_lookup.artist_name.loc[item_lookup.artist_id == idx].iloc[0])
        artist_scores.append(scores[idx])

    similar = pd.DataFrame({'artist': artists, 'score': artist_scores})
    return artists


app = FastAPI()

#for connection with different websites and for Chrome Extension
@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

@app.get("/find_similar_artists", response_model=List[str])
async def find_similar_artists_route(artist: str, num_items: int = 10):
    item_factors, item_biases, item_lookup = load_embeddings()
    similar_artists = find_similar_artists(
        artist, num_items, item_lookup, item_factors, item_biases)
    return similar_artists
