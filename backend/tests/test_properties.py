import pytest
from unittest.mock import MagicMock, patch

def test_create_property_validation_failure(client, mock_admin_auth):
    """Test that creating a property fails if required fields are missing"""
    headers = {'Authorization': 'Bearer admin_token'}
    data = {
        "title": "Test Property"
        # Missing price and type
    }
    response = client.post('/api/properties', json=data, headers=headers)
    assert response.status_code == 400
    assert b"Missing required field" in response.data

def test_create_property_success(client, mock_admin_auth):
    """Test successful property creation"""
    headers = {'Authorization': 'Bearer admin_token'}
    data = {
        "title": "Luxury Villa",
        "price": 10000000,
        "type": "Villa's",
        "location": "Mumbai"
    }
    
    with patch('routes.properties.db') as mock_db:
        # Mock the add operation
        mock_ref = MagicMock()
        mock_ref.id = "new_property_id"
        mock_db.collection.return_value.add.return_value = (None, mock_ref)
        
        # Mock history logging
        with patch('routes.properties.log_property_history'):
             # Mock match checking
            with patch('routes.properties.check_new_listing_matches'):
                response = client.post('/api/properties', json=data, headers=headers)
                
                assert response.status_code == 201
                assert b"new_property_id" in response.data

def test_update_property_validation(client, mock_admin_auth):
    """Test that updating a property with invalid data fails"""
    headers = {'Authorization': 'Bearer admin_token'}
    data = {
        "price": "invalid_price" # Should be number or string number
    }
    
    response = client.put('/api/properties/prop_123', json=data, headers=headers)
    assert response.status_code == 400
    assert b"Invalid price format" in response.data
