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
            salt TEXT NOT NULL,
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

def new_user(username: str, salt: str, auth_verifier: str):
    try:
        with get_connection() as con:
            db_cur = con.cursor()

            db_cur.execute('''
                INSERT INTO users (username, salt, auth_verifier)
                VALUES (?, ?, ?)
            ''', (username, salt, auth_verifier))

            print(f"Sucs: User - {username} sucs made")

            db_cur.close()
    except sqlite3.IntegrityError:
        print(f"Err: User - {username} has already made")

def add_password(user_id: int, encrypted_url: str, encrypted_login: str, encrypted_password: str):
    try:
        with get_connection() as con:
            db_cur = con.cursor()

            db_cur.execute('''
                INSERT INTO passwords (user_id, encrypted_url, encrypted_login, encrypted_password)
                VALUES(?, ?, ?, ?)
            ''', (user_id, encrypted_url, encrypted_login, encrypted_password))

            db_cur.close()
    except Exception as e:
        print(f"Err: {e}")

def get_passwords(user_id: int):
    try:
        with get_connection() as con:
            db_cur = con.cursor()

            db_cur.execute('''
                SELECT id, encrypted_url, encrypted_login, encrypted_password
                FROM passwords
                WHERE user_id = ?
                ''', (user_id,))

            user_dates = db_cur.fetchall()
            
            db_cur.close()

            return user_dates
    except sqlite3.Error as e:
        print(f"Err: {e}")


def get_val(username: str):
    try:
        with get_connection() as con:
            db_cur = con.cursor()

            db_cur.execute('''
                SELECT salt, auth_verifier, id
                FROM users
                WHERE username = ?
            ''', (username,))

            user_data = db_cur.fetchone()

            db_cur.close()

            if user_data:
                return user_data[0], user_data[1], user_data[2]

            print(f"Err: User - {username} doesnt exist")
    except sqlite3.IntegrityError as e:
        print(f"DB err: {e}")



if __name__ == "__main__":
    init_db()