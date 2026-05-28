from dataclasses import dataclass
from typing import Protocol
from repos.in_memory import InMemoryRepository
from repos.json_repo import JsonRepository

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
        user = self.repository.find_by_email(email)
        if user:
            return User(**user)
        else:
            return None


if __name__ == "__main__":
    #in_memory_repo = InMemoryRepository()
    # user_service = UserService(in_memory_repo)
    json_repo = JsonRepository("users.json")
    user_service = UserService(json_repo)
    user1 = User("Alice", "alice@example.com", 30)
    user_service.register(user1)
    print(user_service.find_by_email("alice@example.com"))
