from __future__ import annotations

from repo.storage.in_memory import InMemoryRepository


def test_save_and_find_by_email() -> None:
    repository = InMemoryRepository()
    user = {"name": "Alice", "email": "alice@example.com", "age": 30}

    repository.save(user)

    assert repository.find_by_email("alice@example.com") == user


def test_find_by_email_returns_none_for_unknown_user() -> None:
    repository = InMemoryRepository()

    assert repository.find_by_email("missing@example.com") is None


def test_raises_on_duplicating_email() -> None:
    repository = InMemoryRepository()

    repository.save({"name": "Alice", "email": "alice@example.com", "age": 30})

    try:
        repository.save({"name": "Bob", "email": "alice@example.com", "age": 40})
    except ValueError as exc:
        assert str(exc) == "duplicate email"
    else:
        raise AssertionError("ValueError was not raised")
