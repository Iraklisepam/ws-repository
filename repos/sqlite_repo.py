import sqlite3

class SQLiteRepository:
    def __init__(self, db_path):
        self.db_path = db_path

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                         email TEXT PRIMARY KEY,
                         name TEXT,
                         age INTEGER
                         )
            """)
    
    def save(self, data: dict)->None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO users (name,email,age)
                    VALUES (?,?,?)
            """, (data["name"], data["email"], data["age"]))
        except sqlite3.IntegrityError:
            raise ValueError("duplicate email")
    
    def find_by_email(self, email:str)->dict|None:
        with sqlite3.connect(self.db_path) as conn:
            curr = conn.execute("""
                SELECT * FROM users
                WHERE email = ?
            """, (email,))
            row = curr.fetchone()

        if not row: return None
        
        email, name, age = row

        return {"email": email, "name":name, "age":age}