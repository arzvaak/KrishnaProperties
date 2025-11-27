from flask import Blueprint, request, jsonify
from firebase_config import initialize_firebase
from firebase_admin import firestore, auth
from datetime import datetime

requests_bp = Blueprint('requests', __name__)
db, _ = initialize_firebase()

@requests_bp.route('/api/requests', methods=['POST'])
def create_request():
    try:
        data = request.json
        user_id = data.get('user_id')
        criteria = data.get('criteria') # { minPrice, maxPrice, bedrooms, location, type }
        
        if not user_id or not criteria:
            return jsonify({"error": "User ID and criteria are required"}), 400

        request_data = {
            'user_id': user_id,
            'criteria': criteria,
            'status': 'active',
            'created_at': firestore.SERVER_TIMESTAMP
        }
        
        db.collection('property_requests').add(request_data)

        # Send Notifications
        try:
            from utils.email_service import notify_admin_new_lead, send_request_auto_reply
            
            notify_admin_new_lead('Property Request', request_data)
            
            # Fetch user email for auto-reply
            try:
                user = auth.get_user(user_id)
                if user.email:
                    send_request_auto_reply(user.email, user.display_name or "Valued Customer")
            except Exception as e:
                print(f"Failed to fetch user for auto-reply: {e}")
                
        except Exception as e:
            print(f"Failed to send email notifications: {e}")
        
        return jsonify({"message": "Property request submitted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@requests_bp.route('/api/users/<user_id>/requests', methods=['GET'])
def get_user_requests(user_id):
    try:
        docs = db.collection('property_requests')\
            .where('user_id', '==', user_id)\
            .order_by('created_at', direction=firestore.Query.DESCENDING)\
            .stream()
            
        requests = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            requests.append(data)
            
        return jsonify(requests), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@requests_bp.route('/api/admin/requests', methods=['GET'])
def get_all_requests():
    try:
        docs = db.collection('property_requests')\
            .order_by('created_at', direction=firestore.Query.DESCENDING)\
            .stream()
            
        requests = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            requests.append(data)
            
        return jsonify(requests), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
