# app/database/connection.py

import mysql.connector
from mysql.connector import Error
from app.config import DATABASE_CONFIG

def create_connection():
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None
