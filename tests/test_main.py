import pytest
from pytest_mock import MockerFixture, MockType
from main import UserService, Repository, User


@pytest.fixture
def mock_repo(mocker: MockerFixture) -> MockType:
    return mocker.MagicMock(spec=Repository)


@pytest.fixture
def user_service(mock_repo) -> UserService:
    return UserService(mock_repo)


def test_register_user_converts_to_dict_and_saves(
    user_service: UserService, mock_repo: MockType
):
    user = User(name="alice", email="alice@example.com", age=30)
    user_service.register(user)

    mock_repo.save.assert_called_once_with(
        {"name": "alice", "email": "alice@example.com", "age": 30}
    )


def test_find_by_email_returns_user(user_service: UserService, mock_repo: MockType):
    mock_repo.find_by_email.return_value = {
        "name": "alice",
        "email": "alice@example.com",
        "age": 30,
    }

    user_data = user_service.find_by_email("alice@example.com")
    mock_repo.find_by_email.assert_called_once_with("alice@example.com")

    assert isinstance(user_data, User)
    assert user_data.name == "alice"
    assert user_data.email == "alice@example.com"
    assert user_data.age == 30


def test_find_by_email_returns_none_if_not_found(
    user_service: UserService, mock_repo: MockType
):
    mock_repo.find_by_email.return_value = None
    user_data = user_service.find_by_email("nonexistent@example.com")
    mock_repo.find_by_email.assert_called_once_with("nonexistent@example.com")
    assert user_data is None
