import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.local")

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        dbname=os.getenv('DB_NAME'),
        port=int(os.getenv('DB_PORT', 5432))  # Default to 5432 if not set
    )
    return conn
