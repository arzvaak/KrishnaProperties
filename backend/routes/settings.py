from flask import Blueprint, request, jsonify
from firebase_config import initialize_firebase
from routes.auth import verify_admin

settings_bp = Blueprint('settings', __name__)
db, bucket = initialize_firebase()

# --- Public Endpoints ---

@settings_bp.route('/api/settings/public', methods=['GET'])
def get_public_settings():
    try:
        # Fetch public settings documents
        docs = ['general', 'contact', 'social', 'seo']
        settings = {}
        
        for doc_name in docs:
            doc_ref = db.collection('settings').document(doc_name).get()
            if doc_ref.exists:
                settings[doc_name] = doc_ref.to_dict()
            else:
                settings[doc_name] = {}
                
        return jsonify(settings), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Admin Endpoints ---

@settings_bp.route('/api/admin/settings/<type>', methods=['GET'])
@verify_admin
def get_settings_by_type(type):
    try:
        doc_ref = db.collection('settings').document(type).get()
        if doc_ref.exists:
            return jsonify(doc_ref.to_dict()), 200
        else:
            return jsonify({}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@settings_bp.route('/api/admin/settings/<type>', methods=['PUT'])
@verify_admin
def update_settings(type):
    try:
        data = request.json
        db.collection('settings').document(type).set(data, merge=True)
        return jsonify({"message": "Settings updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
