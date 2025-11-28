import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import datetime

# Initialize Firebase manually to avoid import issues if any
if not firebase_admin._apps:
    cred_path = os.path.join(os.path.dirname(__file__), 'serviceAccountKey.json')
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'krishna-properties-f396d.appspot.com'
    })

db = firestore.client()

def test_queries():
    print("Testing Analytics Queries...")
    
    try:
        print("1. Testing General Stats...")
        stats_doc = db.collection('stats').document('general').get()
        print("   Success.")
    except Exception as e:
        print(f"   FAILED: {e}")

    try:
        print("2. Testing Top Properties Query (requires index)...")
        try:
            props_ref = db.collection('properties')
            top_props_query = props_ref.order_by('views', direction=firestore.Query.DESCENDING).limit(5).stream()
            list(top_props_query) # Trigger execution
            print("   Success.")
        except Exception as e:
            print(f"   Handled Error: {e}")

    except Exception as e:
        print(f"   FAILED: {e}")

    try:
        print("3. Testing Traffic Stats Query (requires index)...")
        try:
            events_query = db.collection('events').where('type', '==', 'site_view') \
                .order_by('timestamp', direction=firestore.Query.DESCENDING).limit(500).stream()
            list(events_query) # Trigger execution
            print("   Success.")
        except Exception as e:
            print(f"   Handled Error: {e}")

    except Exception as e:
        print(f"   FAILED: {e}")

    try:
        print("4. Testing Recent Activity Query (requires index)...")
        try:
            events_ref = db.collection('events').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(10)
            list(events_ref.stream())
            print("   Success.")
        except Exception as e:
            print(f"   Handled Error: {e}")

    except Exception as e:
        print(f"   FAILED: {e}")

    try:
        print("5. Testing Leads & Funnel (unwrapped in backend)...")
        inquiries = list(db.collection('inquiries').stream())
        requests = list(db.collection('property_requests').stream())
        total_leads = len(inquiries) + len(requests)
        print(f"   Found {total_leads} leads.")
        
        funnel = {'new': 0}
        for doc in inquiries + requests:
            data = doc.to_dict()
            status = data.get('status', 'new')
            if hasattr(status, 'lower'):
                status = status.lower()
            else:
                print(f"   Warning: Status is not a string: {status}")
                
            if status in funnel:
                funnel[status] += 1
        print("   Success.")
    except Exception as e:
        print(f"   FAILED: {e}")

if __name__ == "__main__":
    test_queries()
