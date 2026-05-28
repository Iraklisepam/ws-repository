import pytest
from repos.in_memory import InMemoryRepository


@pytest.fixture
def repo():
    return InMemoryRepository()


@pytest.mark.parametrize(
    "email, name, age",
    (("alice@example.com", "alice", 30), ("bob@example.com", "bob", 45)),
)
def test_save(email: str, name: str, age: int, repo: InMemoryRepository):
    data = {"email": email, "name": name, "age": age}
    repo.save(data)

    stored_data = repo.all_data.get(email)
    assert stored_data

    values = stored_data.values()
    assert email in values
    assert name in values
    assert age in values


def test_save_duplicate_email_raises_error(repo: InMemoryRepository):
    data = {"email": "duplicate@example.com", "name": "duplicate", "age": 100}
    repo.save(data)

    with pytest.raises(ValueError, match="duplicate email"):
        repo.save(data)


def test_find_by_email(repo: InMemoryRepository):
    data = {"email": "alice@example.com", "name": "alice", "age": 30}
    repo.save(data)

    found_user = repo.find_by_email(data["email"])
    assert found_user
    assert data == found_user


def test_find_by_email_returns_none_if_not_found(repo: InMemoryRepository):
    found_user = repo.find_by_email("nonexistant@example.com")
    assert found_user is None
