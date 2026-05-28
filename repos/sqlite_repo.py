import sqlite3


class SQLiteRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

        with sqlite3.connect(self.db_path) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    email TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL
                )
            """)

    def save(self, data: dict) -> None:
        try:
            with sqlite3.connect(self.db_path) as connection:
                connection.execute("""
                    INSERT INTO users (name, email, age)
                    VALUES (?, ?, ?)
                """, (data["name"], data["email"], data["age"]))

        except sqlite3.IntegrityError:
            raise ValueError("duplicate email")

    def find_by_email(self, email: str) -> dict | None:
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.execute("""
                SELECT name, email, age
                FROM users
                WHERE email = ?
            """, (email,))

            row = cursor.fetchone()

        if row is None:
            return None

        return {
            "name": row[0],
            "email": row[1],
            "age": row[2],
        }