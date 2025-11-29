from firebase_config import initialize_firebase

db, _ = initialize_firebase()

print("Listing all users in Firestore:")
users = db.collection('users').stream()
for user in users:
    data = user.to_dict()
    print(f"ID: {user.id}, Email: {data.get('email')}, Role: {data.get('role')}")
