import pytest
from unittest.mock import MagicMock
from main import UserService, User

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(mock_repo):
    return UserService(mock_repo)

def test_register_user(service, mock_repo):
    user = User("a", "a@a.a", 30)
    service.register(user)
    mock_repo.save.assert_called_once_with(user.__dict__)

def test_find_by_email(service, mock_repo):
    mock_repo.find_by_email.return_value = {"name": "a", "email": "a@a.a", "age": 30}
    result = service.find_by_email("a@a.a")
    assert result == User("a", "a@a.a", 30)

    mock_repo.find_by_email.return_value = None
    with pytest.raises(TypeError):
        service.find_by_email("b@b.b")