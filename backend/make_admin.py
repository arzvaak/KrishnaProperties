import firebase_admin
from firebase_admin import auth
from firebase_config import initialize_firebase
import sys

initialize_firebase()

def make_admin(email):
    try:
        user = auth.get_user_by_email(email)
        auth.set_custom_user_claims(user.uid, {'admin': True})
        print(f"Success! {email} is now an admin.")
        print(f"User ID: {user.uid}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python make_admin.py <email>")
    else:
        make_admin(sys.argv[1])
