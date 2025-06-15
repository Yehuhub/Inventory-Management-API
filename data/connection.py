import psycopg2

DB_HOST = "localhost"
DB_PORT = "5433"
DB_NAME = "dbname"
DB_USER = "admin"
DB_PASSWORD = "Aa123456"

def get_db_connection():
    conn = psycopg2.connect(
        host = DB_HOST,
        port = DB_PORT,
        database = DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD
    )
    return conn