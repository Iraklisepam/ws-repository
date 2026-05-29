from typing import Optional
from sqlite3 import Connection


class SqlRepo:

    def __init__(self, connection: Connection):
        self.con = connection

        cur = self.con.cursor()
        try:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    age INTEGER NOT NULL
                )
            """)
            self.con.commit()
        finally:
            cur.close()

    def save(self, user: dict) -> None:
        data = self.find_by_email(user["email"])
        if data is not None:
            raise ValueError("duplicate email")
        cur = self.con.cursor()
        try:
            cur.execute("""
                INSERT INTO users (name, email, age)
                VALUES (?, ?, ?)
            """, (user["name"], user["email"], user["age"]))
            self.con.commit()
        finally:
            cur.close()

    def find_by_email(self, email: str) -> Optional[dict]:
        cur = self.con.cursor()
        try:
            cur.execute("""
                SELECT name, email, age
                FROM users
                WHERE email = ?
            """, (email,))
            user_data = cur.fetchone()
            self.con.commit()
        finally:
            cur.close()

        if user_data is None:
            return None

        return {
            "name": user_data[0],
            "email": user_data[1],
            "age": user_data[2]
        }
