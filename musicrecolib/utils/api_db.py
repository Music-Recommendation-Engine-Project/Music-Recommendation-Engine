"""This module contains the DBConnector class which is used to connect to the database and retrieve the data from the database."""

import psycopg2
import pandas as pd

class DBConnector:
    def __init__(self, database_url, dataframe_name):
        self.database_url = database_url 
        self.dataframe_name = dataframe_name
        self.query_standard = f"SELECT * FROM {self.dataframe_name} LIMIT 100000"

    def connect_to_db(self, query=None):
        conn = psycopg2.connect(self.database_url, sslmode='require')
        if conn is None:
            raise psycopg2.OperationalError("Unable to connect to database")
        if query is None:
            query = self.query_standard
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df