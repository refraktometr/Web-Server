import psycopg2
from web_server import db
import json

conn_string = "host='localhost' dbname='web_server' user='postgres' password='postgres'"



all = 1
cursor = db.get_cursor()
cursor.execute("SELECT id, username FROM users")
users_data = cursor.fetchall()
recipient_data = users_data[1]
print users_data[1]
print recipient_data[0]
