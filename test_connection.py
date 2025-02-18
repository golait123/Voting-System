# test_connection.py
from oracledb import connect, DatabaseError

try:
    conn = connect(user="your_username", password="your_password", dsn="localhost:1521/XE")
    print("Connection successful!")
    conn.close()
except DatabaseError as e:
    print("Connection failed:", e)
