import psycopg2
import pandas as pd

# Class to connect to the database
class DBConnector:
    def __init__(self, database_url, dataframe_name):
        self.database_url = database_url  # Database URL for connecting to the database
        self.dataframe_name = dataframe_name  # Name of the table or dataframe to query
        self.query_standard = f"SELECT * FROM {self.dataframe_name} LIMIT 100000"  # Standard query to retrieve data from the table

    def connect_to_db(self, query=None):
        conn = psycopg2.connect(self.database_url, sslmode='require')  # Connect to the database using the provided URL
        if conn is None:
            raise psycopg2.OperationalError("Unable to connect to database")  # Raise an error if the connection is not successful
        if query is None:
            query = self.query_standard  # Use the standard query if no custom query is provided
        df = pd.read_sql_query(query, conn)  # Execute the SQL query and retrieve the data into a pandas DataFrame
        conn.close()  # Close the database connection
        return df  # Return the DataFrame containing the queried data
