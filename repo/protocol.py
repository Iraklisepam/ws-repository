from typing import Protocol, Optional


class Repository(Protocol):

    def save(self, user: dict) -> None:
        ...

    def find_by_email(self, email: str) -> Optional[dict]:
        ...
