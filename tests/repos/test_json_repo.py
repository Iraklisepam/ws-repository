import pytest
import json
from repos.json_repo import JsonRepository


@pytest.fixture
def repo(tmp_path):
    return JsonRepository(tmp_path / "test_repo.json")


@pytest.mark.parametrize(
    "email, name, age",
    (("alice@example.com", "alice", 30), ("bob@example.com", "bob", 45)),
)
def test_save(email: str, name: str, age: int, repo: JsonRepository):
    data = {"email": email, "name": name, "age": age}

    repo.save(data)

    assert repo.all_data.get(email)

    with open(repo.file_path, "r") as f:
        disk_data = json.load(f)

    assert email in disk_data
    assert "name" in disk_data[email]
    assert name in disk_data[email]["name"]


def test_save_duplicate_email_raises_error(repo: JsonRepository):
    data = {"email": "duplicate@example.com", "name": "duplicate", "age": 100}
    repo.save(data)

    with pytest.raises(ValueError, match="duplicate email"):
        repo.save(data)


def test_find_by_email(repo: JsonRepository):
    data = {"email": "alice@example.com", "name": "alice", "age": 30}
    repo.save(data)

    found_user = repo.find_by_email("alice@example.com")
    assert found_user
    assert data == found_user


def test_find_by_email_returns_none_if_not_found(repo: JsonRepository):
    found_user = repo.find_by_email("nonexistant@example.com")
    assert found_user is None
