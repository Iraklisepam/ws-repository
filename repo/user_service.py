from .protocol import Repository
from .user import User


class UserService:
    def __init__(self, repository: Repository):
        self.repository = repository

    def register(self, user: User) -> None:
        self.repository.save(user.__dict__)

    def find_by_email(self, email: str) -> User:
        user_data = self.repository.find_by_email(email)
        if user_data is None:
            raise ValueError("user not found")
        return User(**user_data)
