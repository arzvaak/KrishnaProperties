import requests

BASE_URL = "http://127.0.0.1:5000/api/properties"

def test_cors(origin, expected_allowed):
    headers = {'Origin': origin}
    try:
        response = requests.get(BASE_URL, headers=headers)
        
        # Check Access-Control-Allow-Origin header
        allow_origin = response.headers.get('Access-Control-Allow-Origin')
        
        print(f"Testing Origin: {origin}")
        print(f"Status Code: {response.status_code}")
        print(f"Access-Control-Allow-Origin: {allow_origin}")
        
        if expected_allowed:
            if allow_origin == origin:
                print("PASS: Origin allowed as expected.")
            else:
                print("FAIL: Origin should be allowed but wasn't.")
        else:
            if allow_origin != origin:
                print("PASS: Origin blocked as expected (header missing or different).")
            else:
                print("FAIL: Origin should be blocked but was allowed.")
        print("-" * 30)
        
    except Exception as e:
        print(f"Error: {e}")

print("--- Testing CORS Security ---")

# 1. Test Allowed Origin
test_cors("http://localhost:5173", True)

# 2. Test Blocked Origin
test_cors("http://evil.com", False)
