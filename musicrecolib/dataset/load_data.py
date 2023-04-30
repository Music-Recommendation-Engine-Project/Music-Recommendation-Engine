"""This module contains functions to download the datasets from the database."""

import os
from musicrecolib.utils.api_db import DBConnector

def get_songs():
    dataframe = "songs_df"
    database_url = os.getenv("DATABASE_URL")
    db = DBConnector(database_url, dataframe)
    df = db.connect_to_db()
    return df

def get_users_songs():
    dataframe = "user_track_df"
    database_url = os.getenv("DATABASE_URL")
    db = DBConnector(database_url, dataframe)
    df = db.connect_to_db()
    return df
