import psycopg2
from .config import load_config

def connect():
    config = load_config()
    try:
        connection = psycopg2.connect(**config)
        print("Connection successful!")
        return connection
    except Exception as e:
        print("An error occurred while connecting to the database:", e)

if __name__ == '__main__':
    connect()