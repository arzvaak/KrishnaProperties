from flask import Blueprint, request, jsonify
from firebase_config import initialize_firebase
from firebase_admin import firestore
from datetime import datetime

appointments_bp = Blueprint('appointments', __name__)
db, bucket = initialize_firebase()

@appointments_bp.route('/api/appointments', methods=['POST'])
def create_appointment():
    try:
        data = request.json
        user_id = data.get('user_id')
        property_id = data.get('property_id')
        date = data.get('date')
        time = data.get('time')
        
        if not all([user_id, property_id, date, time]):
            return jsonify({"error": "Missing required fields"}), 400

        # 1. Duplicate Check
        existing_query = db.collection('appointments')\
            .where('user_id', '==', user_id)\
            .where('property_id', '==', property_id)\
            .where('status', '==', 'pending').stream()
            
        if any(existing_query):
            return jsonify({"error": "You already have a pending request for this property."}), 400

        # 2. Rate Limit Check (Max 3 pending requests)
        pending_count_query = db.collection('appointments')\
            .where('user_id', '==', user_id)\
            .where('status', '==', 'pending').stream()
            
        if len(list(pending_count_query)) >= 3:
            return jsonify({"error": "You have reached the limit of 3 active appointment requests. Please wait for a response or cancel one."}), 400

        # Create Appointment
        appointment_data = {
            'user_id': user_id,
            'property_id': property_id,
            'date': date,
            'time': time,
            'status': 'pending',
            'created_at': firestore.SERVER_TIMESTAMP
        }
        
        db.collection('appointments').add(appointment_data)
        
        return jsonify({"message": "Appointment request sent successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@appointments_bp.route('/api/users/<user_id>/appointments', methods=['GET'])
def get_user_appointments(user_id):
    try:
        docs = db.collection('appointments')\
            .where('user_id', '==', user_id)\
            .order_by('created_at', direction=firestore.Query.DESCENDING)\
            .stream()
            
        appointments = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            
            # Fetch property details for context
            if data.get('property_id'):
                p_doc = db.collection('properties').document(data['property_id']).get()
                if p_doc.exists:
                    p_data = p_doc.to_dict()
                    data['property_title'] = p_data.get('title', 'Unknown Property')
                    data['property_image'] = p_data.get('images', [])[0] if p_data.get('images') else p_data.get('imageUrl')
            
            appointments.append(data)
            
        return jsonify(appointments), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
