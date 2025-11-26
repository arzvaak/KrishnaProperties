from flask import Blueprint, request, jsonify
from firebase_config import initialize_firebase
from datetime import datetime

users_bp = Blueprint('users', __name__)
db, _ = initialize_firebase()

@users_bp.route('/api/users/<user_id>/favorites', methods=['POST'])
def add_favorite(user_id):
    try:
        data = request.json
        property_id = data.get('propertyId')
        
        if not property_id:
            return jsonify({"error": "Property ID is required"}), 400

        # Check if property exists
        prop_ref = db.collection('properties').document(property_id)
        if not prop_ref.get().exists:
            return jsonify({"error": "Property not found"}), 404

        # Add to favorites subcollection
        db.collection('users').document(user_id).collection('favorites').document(property_id).set({
            'addedAt': str(datetime.now())
        })
        
        return jsonify({"message": "Added to favorites"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/api/users/<user_id>/favorites/<property_id>', methods=['DELETE'])
def remove_favorite(user_id, property_id):
    try:
        db.collection('users').document(user_id).collection('favorites').document(property_id).delete()
        return jsonify({"message": "Removed from favorites"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/api/users/<user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    try:
        favorites_ref = db.collection('users').document(user_id).collection('favorites')
        docs = favorites_ref.stream()
        
        favorite_ids = [doc.id for doc in docs]
        
        if not favorite_ids:
            return jsonify([]), 200

        # Fetch actual property details for these IDs
        # Note: In a real app, you might want to batch get or store minimal details in favorite doc
        properties = []
        for pid in favorite_ids:
            prop_doc = db.collection('properties').document(pid).get()
            if prop_doc.exists:
                p_data = prop_doc.to_dict()
                p_data['id'] = prop_doc.id
                properties.append(p_data)
                
        return jsonify(properties), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
