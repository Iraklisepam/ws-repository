
class InMemoryRepository:
    def __init__(self):
        self.all_data = {}

    def save(self, data: dict):
        if data['email'] in self.all_data:
            raise ValueError("duplicate email")
        self.all_data[data['email']] = data

    def find_by_email(self, email: str) -> dict | None:
        return self.all_data.get(email)
