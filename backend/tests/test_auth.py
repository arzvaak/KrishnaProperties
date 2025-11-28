from unittest.mock import MagicMock, patch
import json

def test_unauthorized_access(client):
    """Test accessing a protected route without a token"""
    response = client.post('/api/users/sync')
    assert response.status_code == 401

def test_authorized_access(client, mock_auth):
    """Test accessing a protected route with a valid token"""
    # Mock request.user injection which happens in the decorator
    # Since we are mocking verify_id_token, the decorator should work
    
    # We also need to mock the DB call in sync_user to avoid real DB writes
    with patch('routes.users.db') as mock_db:
        # Mock document get
        mock_doc = MagicMock()
        mock_doc.exists = True
        mock_db.collection.return_value.document.return_value.get.return_value = mock_doc
        
        headers = {'Authorization': 'Bearer valid_token'}
        response = client.post('/api/users/sync', headers=headers)
        
        assert response.status_code == 200
        assert b"User synced successfully" in response.data

def test_admin_access_denied_for_user(client, mock_auth):
    """Test that a regular user cannot access admin routes"""
    headers = {'Authorization': 'Bearer user_token'}
    response = client.get('/api/admin/users', headers=headers)
    assert response.status_code == 403

def test_admin_access_granted(client, mock_admin_auth):
    """Test that an admin can access admin routes"""
    with patch('routes.users.db') as mock_db:
        mock_db.collection.return_value.stream.return_value = []
        
        headers = {'Authorization': 'Bearer admin_token'}
        response = client.get('/api/admin/users', headers=headers)
        
        assert response.status_code == 200
