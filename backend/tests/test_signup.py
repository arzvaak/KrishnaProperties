import pytest
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('routes.auth.auth.verify_id_token')
@patch('routes.users.db')
def test_sync_user_new_with_phone(mock_db, mock_verify_id_token, client):
    # Mock token verification result
    mock_verify_id_token.return_value = {
        'uid': 'test_uid_123',
        'email': 'test@example.com',
        'name': 'Test User',
        'picture': 'http://example.com/pic.jpg',
        'role': 'user'
    }

    # Mock Firestore
    mock_user_ref = MagicMock()
    mock_user_doc = MagicMock()
    mock_user_doc.exists = False # New user
    
    mock_user_ref.get.return_value = mock_user_doc
    mock_db.collection.return_value.document.return_value = mock_user_ref

    # Make request with Authorization header
    response = client.post(
        '/api/users/sync', 
        json={'phoneNumber': '+919876543210'},
        headers={'Authorization': 'Bearer mock_token'}
    )
    
    assert response.status_code == 200
    
    # Verify set was called with phone number
    args, _ = mock_user_ref.set.call_args
    saved_data = args[0]
    assert saved_data['email'] == 'test@example.com'
    assert saved_data['phoneNumber'] == '+919876543210'
    assert saved_data['role'] == 'user'

@patch('routes.auth.auth.verify_id_token')
@patch('routes.users.db')
def test_sync_user_new_without_phone_fails(mock_db, mock_verify_id_token, client):
    # Mock token verification result
    mock_verify_id_token.return_value = {
        'uid': 'test_uid_new',
        'email': 'new@example.com'
    }

    # Mock Firestore - New user
    mock_user_ref = MagicMock()
    mock_user_doc = MagicMock()
    mock_user_doc.exists = False 
    
    mock_user_ref.get.return_value = mock_user_doc
    mock_db.collection.return_value.document.return_value = mock_user_ref

    # Make request WITHOUT phone number (Login attempt for new user)
    response = client.post(
        '/api/users/sync', 
        json={},
        headers={'Authorization': 'Bearer mock_token'}
    )
    
    assert response.status_code == 404
    assert "Account not found" in response.get_json()['error']

@patch('routes.auth.auth.verify_id_token')
@patch('routes.users.db')
def test_sync_user_invalid_phone_fails(mock_db, mock_verify_id_token, client):
    # Mock token verification result
    mock_verify_id_token.return_value = {
        'uid': 'test_uid_new',
        'email': 'new@example.com'
    }

    # Mock Firestore - New user
    mock_user_ref = MagicMock()
    mock_user_doc = MagicMock()
    mock_user_doc.exists = False 
    
    mock_user_ref.get.return_value = mock_user_doc
    mock_db.collection.return_value.document.return_value = mock_user_ref

    # Make request with INVALID phone number
    response = client.post(
        '/api/users/sync', 
        json={'phoneNumber': '12345'},
        headers={'Authorization': 'Bearer mock_token'}
    )
    
    assert response.status_code == 400
    assert "Invalid phone number" in response.get_json()['error']

@patch('routes.auth.auth.verify_id_token')
@patch('routes.users.db')
def test_sync_user_existing_update_phone(mock_db, mock_verify_id_token, client):
    # Mock token verification result
    mock_verify_id_token.return_value = {
        'uid': 'test_uid_123',
        'email': 'test@example.com'
    }

    # Mock Firestore - Existing user
    mock_user_ref = MagicMock()
    mock_user_doc = MagicMock()
    mock_user_doc.exists = True 
    
    mock_user_ref.get.return_value = mock_user_doc
    mock_db.collection.return_value.document.return_value = mock_user_ref

    # Make request
    response = client.post(
        '/api/users/sync', 
        json={'phoneNumber': '+919876543210'},
        headers={'Authorization': 'Bearer mock_token'}
    )
    
    assert response.status_code == 200
    
    # Verify update was called with phone number
    args, _ = mock_user_ref.update.call_args
    update_data = args[0]
    assert update_data['phoneNumber'] == '+919876543210'
    assert 'lastLogin' in update_data
