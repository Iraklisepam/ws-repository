from __future__ import annotations

from repo.user_service import UserService
from repo.storage.in_memory import InMemoryRepository
from repo.user import User


def test_register_and_find_user() -> None:
    repository = InMemoryRepository()
    service = UserService(repository)
    user = User("Alice", "alice@example.com", 30)

    service.register(user)

    assert service.find_by_email("alice@example.com") == user


def test_register_duplicate_email_raises() -> None:
    repository = InMemoryRepository()
    service = UserService(repository)
    user = User("Alice", "alice@example.com", 30)

    service.register(user)

    try:
        service.register(user)
    except ValueError as exc:
        assert str(exc) == "duplicate email"
    else:
        raise AssertionError("ValueError was not raised")


def test_find_by_email_raises_if_not_found() -> None:
    repository = InMemoryRepository()
    service = UserService(repository)

    try:
        service.find_by_email("alice@example.com")
    except ValueError as exc:
        assert str(exc) == "user not found"
    else:
        raise AssertionError("ValueError was not raised")
