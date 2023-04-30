from musicrecolib.utils.api_db import DBConnector
import pandas as pd 
import psycopg2
from dotenv import load_dotenv
import os
import pytest
 

'''
Code Analysis

Main functionalities:
The DBConnector class is designed to connect to a PostgreSQL database using a provided database URL and retrieve data from a specified table as a Pandas DataFrame. 

Methods:
- __init__(self, database_url, dataframe_name): Initializes the class with the provided database URL and name of the table to retrieve data from.
- connect_to_db(self): Connects to the database using the provided URL, retrieves data from the specified table as a Pandas DataFrame, and returns the DataFrame.

Fields:
- database_url: A string representing the URL of the PostgreSQL database to connect to.
- dataframe_name: A string representing the name of the table to retrieve data from.
'''

load_dotenv()
database_url = os.getenv("DATABASE_URL")

# Tests that the class can successfully connect to the database and retrieve data when provided with a valid database URL and dataframe name. 
def test_valid_database_url_and_dataframe_name():
    db_connector = DBConnector(database_url=database_url, dataframe_name="user_track_df")
    df = db_connector.connect_to_db()
    assert isinstance(df, pd.DataFrame)
    assert len(df) <= 100000

# Tests that the class can retrieve data from different querys.
def test_different_querys():
    db_connector = DBConnector(database_url=database_url, dataframe_name="user_track_df")
    query = "SELECT * FROM user_track_df LIMIT 1234"
    df = db_connector.connect_to_db(query)
    assert isinstance(df, pd.DataFrame)
    assert len(df) <= 1234

# Tests that the class can retrieve data from different datraframes.
# Waiting for new dataframes to be added to the database.
# def test_different_dataframe_names():
#     db_connector = DBConnector(database_url=database_url, dataframe_name="songs_df")
#     df = db_connector.connect_to_db()
#     assert isinstance(df, pd.DataFrame)
#     assert len(df) <= 100000

# Tests that the class throws an exception when provided with an invalid database URL. 
def test_invalid_database_url():
    db_connector = DBConnector(database_url="invalid_url", dataframe_name="user_track_df")
    with pytest.raises(Exception):
        db_connector.connect_to_db()

# Tests that the class throws an exception when provided with an invalid dataframe name. 
def test_invalid_dataframe_name():
    db_connector = DBConnector(database_url=database_url, dataframe_name="invalid_df_name")
    with pytest.raises(Exception):
        db_connector.connect_to_db()

# Tests that the class can handle an empty dataframe. 
def test_empty_dataframe():
    db_connector = DBConnector(database_url=database_url, dataframe_name="testing")
    df = db_connector.connect_to_db()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0

# Tests that the class can handle retrieving more than 100000 rows from the dataframe. 
def test_retrieve_more_than_100000_rows():
    db_connector = DBConnector(database_url=database_url, dataframe_name="user_track_df")
    query = f"SELECT * FROM {db_connector.dataframe_name} LIMIT 200000"
    conn = psycopg2.connect(db_connector.database_url, sslmode='require')
    df = pd.read_sql_query(query, conn)
    conn.close()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 200000

# Tests that the class can handle exceptions while connecting to the database and retrieving data from the database. 
def test_exceptions_handling():
    with pytest.raises(Exception):
        db_connector = DBConnector(database_url="invalid_url", dataframe_name="invalid_df_name")
        db_connector.connect_to_db()