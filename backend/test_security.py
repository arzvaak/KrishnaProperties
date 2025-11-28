import requests

BASE_URL = "http://127.0.0.1:5000"

def test_endpoint(method, endpoint, token=None, data=None):
    headers = {}
    if token:
        headers['Authorization'] = f"Bearer {token}"
    
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=data)
            
        print(f"{method} {endpoint} - Status: {response.status_code}")
        print(f"Response: {response.text[:100]}...")
        return response.status_code
    except Exception as e:
        print(f"Error: {e}")
        return None

print("--- Testing Security ---")

# 1. Test Admin Blogs (Protected) - No Token
print("\n1. Testing GET /api/admin/blogs (No Token)")
test_endpoint('GET', '/api/admin/blogs')

# 2. Test Admin Blogs (Protected) - Invalid Token
print("\n2. Testing GET /api/admin/blogs (Invalid Token)")
test_endpoint('GET', '/api/admin/blogs', token="invalid_token_123")

# 3. Test Delete Property (Protected) - No Token
print("\n3. Testing DELETE /api/properties/fake_id (No Token)")
test_endpoint('DELETE', '/api/properties/fake_id')

# 4. Test Public Properties (Public) - No Token
print("\n4. Testing GET /api/properties (No Token)")
test_endpoint('GET', '/api/properties')
