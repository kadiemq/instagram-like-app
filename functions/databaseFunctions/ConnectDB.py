import psycopg2
from flask import current_app
from psycopg2.extras import RealDictCursor

def connect_db():
    host = current_app.config['HOST']
    db = current_app.config['DB']
    username = current_app.config['USERNAME']
    password = current_app.config['PASSWORD']
    
    connection = psycopg2.connect(host=host, database=db, user=username, password=password, port=5432, cursor_factory=RealDictCursor)
    return connection
