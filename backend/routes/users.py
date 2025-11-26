from flask import Blueprint, request, jsonify
from firebase_config import initialize_firebase
from firebase_admin import auth, firestore
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

@users_bp.route('/api/users/<user_id>/saved-searches', methods=['POST'])
def save_search(user_id):
    try:
        data = request.json
        # Expected data: { name: "My Search", filters: { minPrice: 0, ... } }
        if not data.get('name') or not data.get('filters'):
            return jsonify({"error": "Name and filters are required"}), 400

        data['createdAt'] = str(datetime.now())
        
        # Add to savedSearches subcollection
        doc_ref = db.collection('users').document(user_id).collection('savedSearches').add(data)
        
        return jsonify({"id": doc_ref[1].id, "message": "Search saved successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/api/users/<user_id>/saved-searches', methods=['GET'])
def get_saved_searches(user_id):
    try:
        searches_ref = db.collection('users').document(user_id).collection('savedSearches')
        docs = searches_ref.stream()
        
        searches = []
        for doc in docs:
            s_data = doc.to_dict()
            s_data['id'] = doc.id
            searches.append(s_data)
            
        return jsonify(searches), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/api/users/<user_id>/saved-searches/<search_id>', methods=['DELETE'])
def delete_saved_search(user_id, search_id):
    try:
        db.collection('users').document(user_id).collection('savedSearches').document(search_id).delete()
        return jsonify({"message": "Saved search deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/api/users/<user_id>/recently-viewed', methods=['POST'])
def add_recently_viewed(user_id):
    try:
        data = request.json
        property_id = data.get('propertyId')
        
        if not property_id:
            return jsonify({"error": "Property ID is required"}), 400

        # Add to recentlyViewed subcollection with timestamp
        # Use set with merge=True to update timestamp if already exists
        db.collection('users').document(user_id).collection('recentlyViewed').document(property_id).set({
            'viewedAt': str(datetime.now()),
            'propertyId': property_id
        }, merge=True)
        
        return jsonify({"message": "Added to recently viewed"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/api/users/<user_id>/recently-viewed', methods=['GET'])
def get_recently_viewed(user_id):
    try:
        # Get recently viewed sorted by viewedAt desc, limit 4
        docs = db.collection('users').document(user_id).collection('recentlyViewed')\
            .order_by('viewedAt', direction=firestore.Query.DESCENDING)\
            .limit(4).stream()
        
        viewed_props = []
        for doc in docs:
            data = doc.to_dict()
            pid = data.get('propertyId')
            if pid:
                # Fetch property details
                p_doc = db.collection('properties').document(pid).get()
                if p_doc.exists:
                    p_data = p_doc.to_dict()
                    p_data['id'] = p_doc.id
                    viewed_props.append(p_data)
            
        return jsonify(viewed_props), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/api/users/<user_id>', methods=['PUT'])
def update_user_profile(user_id):
    try:
        data = request.json
        allowed_fields = ['displayName', 'phoneNumber', 'bio', 'photoURL', 'emailNotifications']
        update_data = {k: v for k, v in data.items() if k in allowed_fields}
        
        if not update_data:
            return jsonify({"error": "No valid fields to update"}), 400

        # Update in Firestore
        db.collection('users').document(user_id).set(update_data, merge=True)
        
        # Update in Auth (DisplayName and PhotoURL only)
        auth_update = {}
        if 'displayName' in update_data:
            auth_update['display_name'] = update_data['displayName']
        if 'photoURL' in update_data:
            auth_update['photo_url'] = update_data['photoURL']
            
        if auth_update:
            auth.update_user(user_id, **auth_update)
            
        return jsonify({"message": "Profile updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/api/users/<user_id>/inquiries', methods=['GET'])
def get_user_inquiries(user_id):
    try:
        # Fetch 'contact' events for this user
        docs = db.collection('events')\
            .where('user_id', '==', user_id)\
            .where('type', '==', 'contact')\
            .order_by('timestamp', direction=firestore.Query.DESCENDING)\
            .stream()
            
        inquiries = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            
            # Fetch property details
            if data.get('property_id'):
                p_doc = db.collection('properties').document(data['property_id']).get()
                if p_doc.exists:
                    p_data = p_doc.to_dict()
                    data['property_title'] = p_data.get('title', 'Unknown Property')
                    data['property_image'] = p_data.get('images', [])[0] if p_data.get('images') else p_data.get('imageUrl')
            
            inquiries.append(data)
            
        return jsonify(inquiries), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        # 1. Delete user document from Firestore
        db.collection('users').document(user_id).delete()
        
        # 2. Delete user from Firebase Auth
        # Note: This is usually done from client side using deleteUser(user), 
        # but having a backend route allows for cleanup of other data if needed.
        # However, the client-side deleteUser is required to invalidate the session properly.
        # The backend delete is for data cleanup.
        # If we want to force delete from backend:
        try:
            auth.delete_user(user_id)
        except Exception as auth_e:
            print(f"Error deleting user from Auth (might be already deleted by client): {auth_e}")

        return jsonify({"message": "User account deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
