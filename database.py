import sqlite3

DB_NAME = "main.db"

def get_connection():
    db_con = sqlite3.connect("main.db")
    db_con.execute("PRAGMA foreign_keys = ON;")
    return db_con

def init_db():
    with get_connection() as con:
        db_cur = con.cursor()

        db_cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            sault TEXT NOT NULL,
            auth_verifier TEXT NOT NULL
        )
        ''')
        db_cur.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            encrypted_url TEXT NOT NULL,
            encrypted_login TEXT NOT NULL,
            encrypted_password TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')

        db_cur.close()

def new_user(username: str, sault: str, auth_verifier: str):
    try:
        with get_connection() as con:
            db_cur = con.cursor()

            db_cur.execute('''
                INSERT INTO users (username, sault, auth_verifier)
                VALUES (?, ?, ?)
            ''', (username, sault, auth_verifier))

            print(f"Sucs: User - {username} sucs made")

            db_cur.close()
    except sqlite3.IntegrityError:
        print(f"Err: User - {username} has already made")

if __name__ == "__main__":
    init_db()