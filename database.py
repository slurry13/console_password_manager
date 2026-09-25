import sqlite3

DB_NAME = "main.db"

def get_connection()
    db_con = sqlite3.connect("main.db")
    db_con.execute("PRAGMA foreign_keys = ON;")
    return db_con

