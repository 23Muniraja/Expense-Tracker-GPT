# test/test_db.py
import pytest
import mysql.connector
from backend.db_helper import get_connection

def test_db_connection():
    conn = get_connection()
    assert conn.is_connected()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]
    assert "expenses" in tables
    cursor.close()
    conn.close()
