import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase Admin SDK (assuming it's already initialized in app context or we do it here)
# Since we are running as a standalone script, we need to initialize it.
# We can reuse the logic from firebase_config.py if possible, or just do it directly.

# Assuming the service account key is at 'backend/serviceAccountKey.json'
cred_path = os.path.join(os.path.dirname(__file__), 'serviceAccountKey.json')
if not os.path.exists(cred_path):
    print(f"Error: serviceAccountKey.json not found at {cred_path}")
    exit(1)

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def delete_collection(coll_ref, batch_size):
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        print(f'Deleting doc {doc.id} => {doc.to_dict().get("title", "No Title")}')
        doc.reference.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

print("Deleting all properties...")
properties_ref = db.collection('properties')
delete_collection(properties_ref, 10)
print("All properties deleted.")
