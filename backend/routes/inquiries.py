from flask import Blueprint, request, jsonify
from firebase_config import initialize_firebase
from firebase_admin import firestore
from datetime import datetime

inquiries_bp = Blueprint('inquiries', __name__)
db, _ = initialize_firebase()

@inquiries_bp.route('/api/inquiries', methods=['POST'])
def create_inquiry():
    try:
        data = request.json
        # Common fields for both contact form and property inquiry
        inquiry_data = {
            'type': data.get('type', 'general'), # 'general' or 'property'
            'name': data.get('name'),
            'email': data.get('email'),
            'message': data.get('message'),
            'subject': data.get('subject'), # Optional
            'property_id': data.get('property_id'), # Optional
            'property_title': data.get('property_title'), # Optional
            'user_id': data.get('user_id'), # Optional, if logged in
            'timestamp': firestore.SERVER_TIMESTAMP,
            'status': 'new' # new, read, replied
        }
        
        if not inquiry_data['email'] or not inquiry_data['message']:
             return jsonify({"error": "Email and message are required"}), 400

        db.collection('inquiries').add(inquiry_data)
        
        # Send Notifications
        try:
            from utils.email_service import notify_admin_new_lead, send_inquiry_auto_reply
            notify_admin_new_lead('Inquiry', inquiry_data)
            if inquiry_data.get('email') and inquiry_data.get('name'):
                send_inquiry_auto_reply(inquiry_data['email'], inquiry_data['name'])
        except Exception as e:
            print(f"Failed to send email notifications: {e}")
        
        return jsonify({"message": "Inquiry sent successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@inquiries_bp.route('/api/admin/inquiries', methods=['GET'])
def get_all_inquiries():
    try:
        docs = db.collection('inquiries')\
            .order_by('timestamp', direction=firestore.Query.DESCENDING)\
            .stream()
            
        inquiries = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            inquiries.append(data)
            
        return jsonify(inquiries), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@inquiries_bp.route('/api/users/<user_id>/inquiries', methods=['GET'])
def get_user_inquiries(user_id):
    try:
        docs = db.collection('inquiries')\
            .where('user_id', '==', user_id)\
            .order_by('timestamp', direction=firestore.Query.DESCENDING)\
            .stream()
            
        inquiries = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            inquiries.append(data)
            
        return jsonify(inquiries), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
