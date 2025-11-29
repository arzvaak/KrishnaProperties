from firebase_config import initialize_firebase
from firebase_admin import auth

db, _ = initialize_firebase()

uid = 'XXaN1IhnzhaWl4EVlWL3a4js4rE3'
print(f"Fixing role for {uid}...")

# Update Firestore
db.collection('users').document(uid).update({'role': 'superadmin'})

# Update Auth Claims
auth.set_custom_user_claims(uid, {'role': 'superadmin'})

print("Role updated to superadmin.")
