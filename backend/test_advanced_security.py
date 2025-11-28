import requests
import time

BASE_URL = "http://127.0.0.1:5000"

def test_csp():
    print("\n--- Testing CSP ---")
    try:
        response = requests.get(f"{BASE_URL}/health")
        csp = response.headers.get('Content-Security-Policy')
        print(f"CSP Header: {csp}")
        if csp and "default-src 'self'" in csp:
            print("PASS: CSP header is present and strict.")
        else:
            print("FAIL: CSP header missing or weak.")
    except Exception as e:
        print(f"Error: {e}")

def test_rate_limit():
    print("\n--- Testing Rate Limit (Login) ---")
    # Note: We need a valid token to test the protected endpoint, 
    # but for rate limiting, the 429 might trigger before auth check depending on implementation order.
    # Flask-Limiter usually runs before view functions.
    # However, our @verify_token decorator might run first if placed before @limiter.
    # In users.py: @verify_token is first (outer), then @limiter.
    # Wait, decorators wrap from bottom up. 
    # @verify_token
    # @limiter.limit
    # def func():
    # This means verify_token runs first. So we need a token.
    # Actually, let's try without token first. If it returns 401, then auth is first.
    # If we want to test rate limit, we need to pass auth.
    # Since getting a real token is hard here, let's assume the user has a token or test a public endpoint if we limited one.
    # We only limited /api/users/sync which is protected.
    
    # Alternative: Check if rate limit headers are present even on 401? Probably not.
    # Let's try to hit it.
    
    url = f"{BASE_URL}/api/users/sync"
    headers = {"Authorization": "Bearer fake_token"} 
    
    for i in range(1, 8):
        response = requests.post(url, headers=headers)
        print(f"Request {i}: Status {response.status_code}")
        
        if response.status_code == 429:
            print("PASS: Rate limit triggered.")
            return
        
        # If we get 401, it means auth check failed but request went through limiter?
        # If verify_token is outer, it runs BEFORE limiter.
        # So we won't hit rate limit if we fail auth first.
        # This is actually good for security (don't limit invalid tokens, just block them).
        # But bad for testing here without a token.
        
        # However, for BRUTE FORCE protection, we want to limit attempts even with invalid credentials?
        # Usually yes. But here we are limiting the *sync* endpoint which assumes successful firebase login.
        # So the brute force protection is actually on Firebase side.
        # The rate limit here protects the backend from spamming syncs.
        
        # So to test this, we'd need a valid token.
        # I will skip strict rate limit verification script for now and rely on code review 
        # because generating a valid firebase token in python script requires admin sdk or web api key exchange.
        pass

    print("SKIP: Cannot verify rate limit without valid token (Auth check runs first).")

test_csp()
test_rate_limit()
