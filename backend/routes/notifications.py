from flask import Blueprint, request, jsonify
from firebase_admin import firestore
from functools import wraps
from routes.auth import verify_token

notifications_bp = Blueprint('notifications', __name__)
db = firestore.client()

@notifications_bp.route('/', methods=['GET'])
@verify_token
def get_notifications(user_data):
    try:
        uid = user_data['uid']
        # Get last 50 notifications
        docs = db.collection('users').document(uid).collection('notifications')\
            .order_by('createdAt', direction=firestore.Query.DESCENDING)\
            .limit(50).stream()
        
        notifications = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            notifications.append(data)
            
        return jsonify(notifications), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notifications_bp.route('/<notification_id>/read', methods=['PUT'])
@verify_token
def mark_as_read(user_data, notification_id):
    try:
        uid = user_data['uid']
        doc_ref = db.collection('users').document(uid).collection('notifications').document(notification_id)
        doc_ref.update({'read': True})
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notifications_bp.route('/read-all', methods=['PUT'])
@verify_token
def mark_all_as_read(user_data):
    try:
        uid = user_data['uid']
        batch = db.batch()
        docs = db.collection('users').document(uid).collection('notifications').where('read', '==', False).stream()
        
        count = 0
        for doc in docs:
            batch.update(doc.reference, {'read': True})
            count += 1
            
        if count > 0:
            batch.commit()
            
        return jsonify({'success': True, 'count': count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notifications_bp.route('/<notification_id>', methods=['DELETE'])
@verify_token
def delete_notification(user_data, notification_id):
    try:
        uid = user_data['uid']
        db.collection('users').document(uid).collection('notifications').document(notification_id).delete()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notifications_bp.route('/preferences', methods=['GET', 'POST'])
@verify_token
def handle_preferences(user_data):
    try:
        uid = user_data['uid']
        pref_ref = db.collection('users').document(uid).collection('settings').document('notifications')
        
        if request.method == 'GET':
            doc = pref_ref.get()
            if not doc.exists:
                # Default preferences
                return jsonify({
                    'email': True,
                    'push': True,
                    'marketing': False,
                    'security': True
                }), 200
            return jsonify(doc.to_dict()), 200
            
        elif request.method == 'POST':
            data = request.json
            pref_ref.set(data, merge=True)
            return jsonify({'success': True}), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
