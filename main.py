import sqlite3
from dataclasses import dataclass
from typing import Protocol
from repos.in_memory import InMemoryRepository
from repos.json_repo import JsonRepository
from repos.sqlite_repo import SQLiteRepository


@dataclass
class User:
    name: str
    email: str
    age: int


class Repository(Protocol):
    def save(self, data: dict) -> None: ...
    def find_by_email(self, email: str) -> dict | None: ...


class UserService:
    def __init__(self, repository: Repository):
        self.repository = repository

    def register(self, user: User) -> None:
        self.repository.save(user.__dict__)

    def find_by_email(self, email: str) -> User | None:
        user_data = self.repository.find_by_email(email)
        return User(**user_data) if user_data else None


def _init_db(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    query = """
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, 
        name TEXT,
        email TEXT UNIQUE,
        age INTEGER 
        )
"""
    cursor.execute(query)
    conn.commit()


if __name__ == "__main__":
    # in_memory_repo = InMemoryRepository()
    # user_service = UserService(in_memory_repo)

    # json_repo = JsonRepository("users.json")
    # user_service = UserService(json_repo)
    with sqlite3.connect("users.db") as conn:
        _init_db(conn)
        sqlite_repo = SQLiteRepository(conn)
        user_service = UserService(sqlite_repo)

        user1 = User("Alice", "alice@example.com", 30)
        user_service.register(user1)
        print(user_service.find_by_email("alice@example.com"))
