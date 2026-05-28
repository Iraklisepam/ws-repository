import sqlite3


class SQLiteRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def save(self, data):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                (data["name"], data["email"], data["age"]),
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError("duplicate email")

    def find_by_email(self, email):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, email, age FROM users WHERE email=?", (email,))
        data = cursor.fetchone()
        if not data:
            return None
        name, email, age = data
        return {"name": name, "email": email, "age": age}
