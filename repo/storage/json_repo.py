import json

from typing import Optional
from os import PathLike


class JsonRepository:

    def __init__(self, file_path: PathLike[str]):
        self.file_path = file_path
        self.all_data = self._get_all_data()

    def _get_all_data(self):
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save(self, data: dict) -> None:
        if data['email'] in self.all_data:
            raise ValueError("duplicate email")
        self.all_data[data['email']] = data
        with open(self.file_path, 'w') as f:
            json.dump(self.all_data, f)

    def find_by_email(self, email: str) -> Optional[dict]:
        data = self.all_data.get(email)
        if data:
            return data
        return None

