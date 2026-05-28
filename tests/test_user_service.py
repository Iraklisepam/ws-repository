import pytest

from main import User, UserService
from repos.in_memory import InMemoryRepository
from repos.json_repo import JsonRepository
from repos.sqlite_repo import SQLiteRepository


def create_repository(repo_type: str, tmp_path):
    if repo_type == "memory":
        return InMemoryRepository()

    if repo_type == "json":
        return JsonRepository(str(tmp_path / "users.json"))

    if repo_type == "sqlite":
        return SQLiteRepository(str(tmp_path / "users.db"))

    raise ValueError(f"Unknown repository type: {repo_type}")


@pytest.mark.parametrize("repo_type", ["memory", "json", "sqlite"])
def test_register_and_find_user(repo_type, tmp_path):
    repository = create_repository(repo_type, tmp_path)
    user_service = UserService(repository)

    user = User("Alice", "alice@example.com", 30)

    user_service.register(user)

    found_user = user_service.find_by_email("alice@example.com")

    assert found_user == User("Alice", "alice@example.com", 30)


@pytest.mark.parametrize("repo_type", ["memory", "json", "sqlite"])
def test_duplicate_email_raises_error(repo_type, tmp_path):
    repository = create_repository(repo_type, tmp_path)
    user_service = UserService(repository)

    user = User("Alice", "alice@example.com", 30)

    user_service.register(user)

    with pytest.raises(ValueError, match="duplicate email"):
        user_service.register(user)


@pytest.mark.parametrize("repo_type", ["memory", "json", "sqlite"])
def test_register_multiple_users(repo_type, tmp_path):
    repository = create_repository(repo_type, tmp_path)
    user_service = UserService(repository)

    user1 = User("Alice", "alice@example.com", 30)
    user2 = User("Bob", "bob@example.com", 25)

    user_service.register(user1)
    user_service.register(user2)

    assert user_service.find_by_email("alice@example.com") == User(
        "Alice",
        "alice@example.com",
        30,
    )

    assert user_service.find_by_email("bob@example.com") == User(
        "Bob",
        "bob@example.com",
        25,
    )