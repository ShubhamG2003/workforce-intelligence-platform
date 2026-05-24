import os

DB_PASSWORD = os.getenv("DB_PASSWORD")

DB_CONFIG = {
    "user": "insert_username",
    "password": DB_PASSWORD,
    "host": "localhost",
    "port": 5432,
    "db": "workforce_db"
}
