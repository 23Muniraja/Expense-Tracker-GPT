# backend/db_helper.py

import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',       # your MySQL username
            password='muni',   # your MySQL password
            database='expense_manager'  # your database name
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
