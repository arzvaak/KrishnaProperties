import firebase_admin
from firebase_admin import auth
from firebase_config import initialize_firebase
import sys

initialize_firebase()

def make_admin(email):
    try:
        user = auth.get_user_by_email(email)
        uid = user.uid
        
        # 1. Update Firestore
        from firebase_admin import firestore
        db = firestore.client()
        db.collection('users').document(uid).update({'role': 'admin'})
        print(f"Updated Firestore role for {email}")

        # 2. Update Custom Claims (support both 'admin': True and 'role': 'admin')
        auth.set_custom_user_claims(uid, {'admin': True, 'role': 'admin'})
        print(f"Success! {email} is now an admin.")
        print(f"User ID: {uid}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python make_admin.py <email>")
    else:
        make_admin(sys.argv[1])
