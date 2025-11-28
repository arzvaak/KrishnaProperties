from flask import Blueprint, request, jsonify
from firebase_config import initialize_firebase
from firebase_admin import firestore, auth
from datetime import datetime
from routes.auth import verify_token, verify_admin

appointments_bp = Blueprint('appointments', __name__)
db, bucket = initialize_firebase()

@appointments_bp.route('/api/appointments', methods=['POST'])
@verify_token
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
        
        # Send Email Notification
        try:
            from utils.email_service import notify_appointment_confirmation, notify_admin_new_lead, notify_appointment_status_change, notify_appointment_reschedule
            
            # Notify Admin
            notify_admin_new_lead('Appointment', appointment_data)

            # Notify User
            user = auth.get_user(user_id)
            if user.email:
                # Fetch property title for the email
                prop_doc = db.collection('properties').document(property_id).get()
                prop_title = prop_doc.to_dict().get('title', 'Property') if prop_doc.exists else 'Property'
                
                notify_appointment_confirmation(user.email, prop_title, date, time)
        except Exception as e:
            print(f"Failed to send email: {e}")

        return jsonify({"message": "Appointment request sent successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@appointments_bp.route('/api/users/<user_id>/appointments', methods=['GET'])
@verify_token
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

@appointments_bp.route('/api/admin/appointments', methods=['GET'])
@verify_admin
def get_all_appointments():
    try:
        docs = db.collection('appointments')\
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

@appointments_bp.route('/api/appointments/<appointment_id>/status', methods=['PATCH'])
@verify_admin
def update_appointment_status(appointment_id):
    try:
        data = request.json
        status = data.get('status')
        
        if status not in ['confirmed', 'completed', 'cancelled']:
            return jsonify({"error": "Invalid status"}), 400
            
        # Update Firestore
        doc_ref = db.collection('appointments').document(appointment_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return jsonify({"error": "Appointment not found"}), 404
            
        doc_ref.update({'status': status})
        
        # Send Email Notification
        try:
            from utils.email_service import notify_appointment_status_change
            
            appt_data = doc.to_dict()
            user_id = appt_data.get('user_id')
            property_id = appt_data.get('property_id')
            date = appt_data.get('date')
            time = appt_data.get('time')
            
            user = auth.get_user(user_id)
            if user.email:
                prop_doc = db.collection('properties').document(property_id).get()
                prop_title = prop_doc.to_dict().get('title', 'Property') if prop_doc.exists else 'Property'
                
                notify_appointment_status_change(user.email, prop_title, date, time, status)
        except Exception as e:
            print(f"Failed to send email: {e}")
            
        return jsonify({"message": f"Appointment status updated to {status}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@appointments_bp.route('/api/appointments/<appointment_id>/reschedule', methods=['PATCH'])
@verify_admin
def reschedule_appointment(appointment_id):
    try:
        data = request.json
        new_date = data.get('date')
        new_time = data.get('time')
        
        if not new_date or not new_time:
            return jsonify({"error": "Missing date or time"}), 400
            
        # Update Firestore
        doc_ref = db.collection('appointments').document(appointment_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return jsonify({"error": "Appointment not found"}), 404
            
        appt_data = doc.to_dict()
        old_date = appt_data.get('date')
        old_time = appt_data.get('time')
        
        doc_ref.update({
            'date': new_date,
            'time': new_time,
            'status': 'confirmed' # Auto-confirm if admin reschedules
        })
        
        # Send Email Notification
        try:
            from utils.email_service import notify_appointment_reschedule
            
            user_id = appt_data.get('user_id')
            property_id = appt_data.get('property_id')
            
            user = auth.get_user(user_id)
            if user.email:
                prop_doc = db.collection('properties').document(property_id).get()
                prop_title = prop_doc.to_dict().get('title', 'Property') if prop_doc.exists else 'Property'
                
                notify_appointment_reschedule(user.email, prop_title, old_date, old_time, new_date, new_time)
        except Exception as e:
            print(f"Failed to send email: {e}")
            
        return jsonify({"message": "Appointment rescheduled successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
