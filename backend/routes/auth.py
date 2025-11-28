from functools import wraps
from flask import request, jsonify
from firebase_admin import auth

def verify_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'No token provided'}), 401
        
        try:
            # Expecting 'Bearer <token>'
            token = auth_header.split(' ')[1]
            decoded_token = auth.verify_id_token(token)
            request.user = decoded_token
        except Exception as e:
            print(f"Token verification error: {e}")
            return jsonify({'error': 'Invalid token'}), 401
            
        return f(*args, **kwargs)
    return decorated_function

def verify_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'No token provided'}), 401
        
        try:
            token = auth_header.split(' ')[1]
            decoded_token = auth.verify_id_token(token)
            # print(f"Admin Verify - Decoded Token: {decoded_token}")
            
            # Check if user has admin claim or specific email
            # For this project, we might just check email or a custom claim
            # Assuming 'admin' claim or specific email for now
            if not decoded_token.get('admin') and decoded_token.get('email') != 'admin@krishnarealestate.com' and decoded_token.get('role') not in ['admin', 'superadmin']:
                print(f"Unauthorized access attempt by: {decoded_token.get('email')}")
                return jsonify({'error': 'Unauthorized: Admin privileges required'}), 403
            
            request.user = decoded_token
        except Exception as e:
            return jsonify({'error': 'Invalid token'}), 401
            
        return f(*args, **kwargs)
    return decorated_function
