
class InMemoryRepository:
    def __init__(self):
        self.users = {}

    def save(self, data: dict) -> None:
        if data['email'] in self.users:
            raise ValueError("duplicate email")
        self.users[data['email']] = data

    def find_by_email(self, email: str) -> dict | None:
        return self.users.get(email, None)
