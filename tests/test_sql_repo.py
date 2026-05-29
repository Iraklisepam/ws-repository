from __future__ import annotations

import sqlite3

from repo.storage.sql_repo import SqlRepo


def test_save_and_find_by_email() -> None:
    connection = sqlite3.connect(":memory:")
    repository = SqlRepo(connection)
    user = {"name": "Alice", "email": "alice@example.com", "age": 30}

    try:
        repository.save(user)

        assert repository.find_by_email("alice@example.com") == user
    finally:
        connection.close()


def test_find_by_email_returns_none_for_unknown_user() -> None:
    connection = sqlite3.connect(":memory:")
    repository = SqlRepo(connection)

    try:
        assert repository.find_by_email("missing@example.com") is None
    finally:
        connection.close()


def test_raises_on_duplicating_email() -> None:
    connection = sqlite3.connect(":memory:")
    repository = SqlRepo(connection)

    repository.save({"name": "Alice", "email": "alice@example.com", "age": 30})

    try:
        repository.save({"name": "Bob", "email": "alice@example.com", "age": 40})
    except ValueError as exc:
        assert str(exc) == "duplicate email"
    else:
        raise AssertionError("ValueError was not raised")
