"""This module contains functions to download the datasets from the database."""

import os
from musicrecolib.utils.api_db import DBConnector
from dotenv import load_dotenv

# Class to load the data from the database
class LoadData:
    def __init__(self, query=None):
        self.query = query  # Custom query to retrieve specific data (optional)
        
    def get_songs(self, query=None):
        dataframe = "songs_df"  # Name of the table or dataframe for songs
        load_dotenv()  # Load environment variables from the .env file
        database_url = os.getenv("DATABASE_URL")  # Get the database URL from the environment variables
        db = DBConnector(database_url, dataframe)  # Create a DBConnector instance to connect to the database and retrieve data for songs
        df = db.connect_to_db(query)  # Connect to the database and execute the query to retrieve songs data
        return df  # Return the DataFrame containing the songs data

    def get_users_songs(self, query=None):
        dataframe = "user_track_df"  # Name of the table or dataframe for user tracks
        load_dotenv()  # Load environment variables from the .env file
        database_url = os.getenv("DATABASE_URL")  # Get the database URL from the environment variables
        db = DBConnector(database_url=database_url, dataframe_name=dataframe)  # Create a DBConnector instance to connect to the database and retrieve data for user tracks
        df = db.connect_to_db(query)  # Connect to the database and execute the query to retrieve user tracks data
        return df  # Return the DataFrame containing the user tracks data
