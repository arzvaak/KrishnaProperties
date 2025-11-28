import pytest
import sys
import os

# Add backend directory to path so we can import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app

@pytest.fixture
def app():
    # Force debug to True to disable Talisman HTTPS redirect
    os.environ['FLASK_DEBUG'] = 'True'
    flask_app.config.update({
        "TESTING": True,
        "DEBUG": True
    })
    yield flask_app
    # Cleanup
    os.environ.pop('FLASK_DEBUG', None)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def mock_auth(mocker):
    """Mocks Firebase Auth verify_id_token"""
    mock = mocker.patch('firebase_admin.auth.verify_id_token')
    mock.return_value = {
        'uid': 'test_user_id',
        'email': 'test@example.com',
        'name': 'Test User',
        'picture': 'http://example.com/pic.jpg',
        'role': 'user'
    }
    return mock

@pytest.fixture
def mock_admin_auth(mocker):
    """Mocks Firebase Auth verify_id_token for Admin"""
    mock = mocker.patch('firebase_admin.auth.verify_id_token')
    mock.return_value = {
        'uid': 'admin_user_id',
        'email': 'admin@example.com',
        'role': 'admin'
    }
    return mock
