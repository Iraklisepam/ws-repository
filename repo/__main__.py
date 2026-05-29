import sqlite3

# from .storage.json_repo import JsonRepository
# from .storage.in_memory import InMemoryRepository
from .storage.sql_repo import SqlRepo

from .user import User
from .user_service import UserService


def main():
    # in_memory_repo = InMemoryRepository()
    # user_service = UserService(in_memory_repo)

    # json_repo = JsonRepository("users.json")
    # user_service = UserService(json_repo)

    con = sqlite3.connect("example.db")
    try:
        sql_repo = SqlRepo(con)
        user_service = UserService(sql_repo)

        user1 = User("Alice", "alice@example.com", 30)
        user_service.register(user1)

        print(user_service.find_by_email("alice@example.com"))
    finally:
        con.close()

    return 0


if __name__ == "__main__":
    exit(main())
