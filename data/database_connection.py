import psycopg2
from contextlib import contextmanager
from dotenv import load_dotenv
import os 

"""
This module provides a class to manage database connections and execute queries.
It uses psycopg2 to connect to a PostgreSQL database and contextlib for managing connections.

To use this module:
1) Set up a .env file with the Database connection details
    DB_HOST=your_host
    DB_NAME=your_database_name
    DB_USER=your_username
    DB_PASSWORD=your_password
    DB_PORT=your_port (optional, defaults to 5432)

2) Instantiate a DatabaseConnection object and use the `get_connection` method to obtain a connection context.
Example usage:
    db_conn = DatabaseConnection()

    with db_conn.get_connection() as conn:
        cur = conn.cursor()

"""

# Load environment variables from .env file
load_dotenv()

# Class to manage database connections and execute queries
class DatabaseConnection:
    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.dbname = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.port = os.getenv('DB_PORT', 5432)  # Default PostgreSQL port is 5432,
        
    @contextmanager
    def get_connection(self):
        # Returns the database connection object
        conn = None
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            yield conn
        except psycopg2.Error as e:
            if conn:
                conn.rollback() # Rollback any changes if an error occurs (maintain consistency)
            raise e
        finally:
            if conn:
                conn.close()