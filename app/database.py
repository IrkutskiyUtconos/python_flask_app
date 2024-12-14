import sqlite3
from app.scraper import scrape_and_save

def get_db_connection():
    conn = sqlite3.connect('app/recipes.db')
    conn.row_factory = sqlite3.Row
    return conn