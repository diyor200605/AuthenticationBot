import sqlite3


def init_db():
    with sqlite3.connect('auth.db') as conn:
        cur = conn.cursor()
        cur.execute(""" 
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tg_id INTEGER,
                    username TEXT UNIQUE,
                    password TEXT,
                    email TEXT
                )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                tg_id INTEGER PRIMARY KEY,
                is_logged INTEGER DEFAULT 0
            )            
        """)
        conn.commit()


def register_user(username: str, password: str, tg_id: int):
    with sqlite3.connect('auth.db') as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password, tg_id) VALUES (?,?,?)", (username, password, tg_id))
        cur.execute("INSERT OR REPLACE INTO sessions (tg_id, is_logged) VALUES (?, 1)", (tg_id,))
        conn.commit()


def check_user(username: str, password: str):
    with sqlite3.connect('auth.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT tg_id FROM users WHERE  username=? AND password=?", (username, password))
        row = cur.fetchone()
        if row:
            return True, row[0]
        return False, None


def is_logged(tg_id: int):
    with sqlite3.connect('auth.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT is_logged FROM sessions WHERE tg_id=?", (tg_id,))
        row = cur.fetchone()
        return row and row[0] == 1


def set_logged(tg_id: int, flag: int):
    with sqlite3.connect('auth.db') as conn:
        cur = conn.cursor()
        cur.execute("INSERT OR REPLACE INTO sessions (tg_id, is_logged) VALUES (?,?)", (tg_id, flag))
        conn.commit()


def username_exists(username: str):
    with sqlite3.connect('auth.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE username=?", (username,))
        return cur.fetchone() is not None