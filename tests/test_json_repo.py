from __future__ import annotations

import json

from repo.storage.json_repo import JsonRepository


def test_save_and_find_by_email(tmp_path) -> None:
    file_path = tmp_path / "users.json"
    repository = JsonRepository(file_path)
    user = {"name": "Alice", "email": "alice@example.com", "age": 30}

    repository.save(user)

    assert repository.find_by_email("alice@example.com") == user


def test_save_persists_to_disk(tmp_path) -> None:
    file_path = tmp_path / "users.json"
    repository = JsonRepository(file_path)

    repository.save({"name": "Alice", "email": "alice@example.com", "age": 30})

    assert json.loads(file_path.read_text()) == {
        "alice@example.com": {
            "name": "Alice",
            "email": "alice@example.com",
            "age": 30,
        }
    }


def test_raises_on_duplicating_email(tmp_path) -> None:
    file_path = tmp_path / "users.json"
    repository = JsonRepository(file_path)

    repository.save({"name": "Alice", "email": "alice@example.com", "age": 30})

    try:
        repository.save({"name": "Bob", "email": "alice@example.com", "age": 40})
    except ValueError as exc:
        assert str(exc) == "duplicate email"
    else:
        raise AssertionError("ValueError was not raised")
