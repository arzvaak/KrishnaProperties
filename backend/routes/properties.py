from flask import Blueprint, request, jsonify
from firebase_config import initialize_firebase
from firebase_admin import firestore, auth
from utils.email_service import notify_saved_search_match, notify_price_drop

properties_bp = Blueprint('properties', __name__)
db, bucket = initialize_firebase()

@properties_bp.route('/api/properties', methods=['GET'])
def get_properties():
    try:
        properties_ref = db.collection('properties')
        
        # Get query parameters
        min_price = request.args.get('min_price', type=int)
        max_price = request.args.get('max_price', type=int)
        bedrooms = request.args.get('bedrooms', type=int)
        prop_type = request.args.get('type')
        search = request.args.get('search', '').lower()
        sort_by = request.args.get('sort', 'newest')
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 9, type=int)

        # Firestore filtering (basic)
        query = properties_ref
        if prop_type:
            query = query.where('type', '==', prop_type)
        if bedrooms:
            query = query.where('bedrooms', '>=', bedrooms)
            
        docs = query.stream()
        properties = []
        
        for doc in docs:
            prop_data = doc.to_dict()
            prop_data['id'] = doc.id
            
            # In-memory filtering for fields that might be complex to index or string matching
            # Price parsing (assuming stored as string "₹ 1,50,00,000")
            try:
                price_str = prop_data.get('price', '0').replace('₹', '').replace(',', '').strip()
                price = int(price_str)
            except:
                price = 0
                
            if min_price is not None and price < min_price:
                continue
            if max_price is not None and price > max_price:
                continue
                
            # Search filter (Title or Location)
            if search:
                title = prop_data.get('title', '').lower()
                location = prop_data.get('location', '').lower()
                if search not in title and search not in location:
                    continue
                    
            properties.append(prop_data)
            
        # Sorting
        if sort_by == 'price_asc':
            properties.sort(key=lambda x: int(str(x.get('price', '0')).replace('₹', '').replace(',', '').strip()) if x.get('price') else 0)
        elif sort_by == 'price_desc':
            properties.sort(key=lambda x: int(str(x.get('price', '0')).replace('₹', '').replace(',', '').strip()) if x.get('price') else 0, reverse=True)
        else: # newest (default)
            # Assuming documents have a timestamp or we use ID/natural order if no timestamp
            # For now, reverse list as Firestore returns oldest first by default usually
            properties.reverse()

        # Pagination
        total = len(properties)
        total_pages = (total + limit - 1) // limit
        start = (page - 1) * limit
        end = start + limit
        paginated_properties = properties[start:end]
        
        return jsonify({
            "properties": paginated_properties,
            "total": total,
            "page": page,
            "total_pages": total_pages
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@properties_bp.route('/api/properties', methods=['POST'])
def create_property():
    try:
        data = request.json
        # TODO: Add validation and admin check
        update_time, property_ref = db.collection('properties').add(data)
        
        # Check for matches
        try:
            check_new_listing_matches(data, property_ref.id)
        except Exception as e:
            print(f"Error checking matches: {e}")

        return jsonify({"id": property_ref.id, "message": "Property created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@properties_bp.route('/api/properties/<property_id>', methods=['GET'])
def get_property(property_id):
    try:
        doc_ref = db.collection('properties').document(property_id)
        doc = doc_ref.get()
        if doc.exists:
            prop_data = doc.to_dict()
            prop_data['id'] = doc.id
            return jsonify(prop_data), 200
        else:
            return jsonify({"error": "Property not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@properties_bp.route('/api/properties/<property_id>', methods=['DELETE'])
def delete_property(property_id):
    try:
        db.collection('properties').document(property_id).delete()
        return jsonify({"message": "Property deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@properties_bp.route('/api/properties/<property_id>', methods=['PUT'])
def update_property(property_id):
    try:
        data = request.json
        
        # Check for price drop before updating
        try:
            check_price_drop(property_id, data)
        except Exception as e:
            print(f"Error checking price drop: {e}")

        db.collection('properties').document(property_id).update(data)
        return jsonify({"message": "Property updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def parse_price(price_str):
    try:
        return int(str(price_str).replace('₹', '').replace(',', '').strip())
    except:
        return 0

def check_new_listing_matches(property_data, property_id):
    # 1. Check Property Requests (Global collection)
    requests_ref = db.collection('property_requests').where('status', '==', 'active').stream()
    
    prop_price = parse_price(property_data.get('price'))
    prop_bedrooms = int(property_data.get('bedrooms', 0))
    prop_type = property_data.get('type')
    prop_location = property_data.get('location', '').lower()

    for req in requests_ref:
        req_data = req.to_dict()
        criteria = req_data.get('criteria', {})
        user_id = req_data.get('user_id')
        
        # Check criteria
        min_price = int(criteria.get('minPrice', 0))
        max_price = int(criteria.get('maxPrice', 1000000000))
        req_bedrooms = int(criteria.get('bedrooms', 0))
        req_type = criteria.get('type')
        req_location = criteria.get('location', '').lower()

        if min_price <= prop_price <= max_price:
            if prop_bedrooms >= req_bedrooms:
                if not req_type or req_type == 'any' or req_type == prop_type:
                    if not req_location or req_location in prop_location:
                        # Match found!
                        try:
                            user = auth.get_user(user_id)
                            if user.email:
                                notify_saved_search_match(user.email, "Property Request Match", property_data.get('title'), property_id)
                        except:
                            pass

    # 2. Check Saved Searches (Per User)
    # Note: Iterating all users is inefficient. In production, use a dedicated 'saved_searches' collection group query.
    # For MVP, we'll skip complex user iteration or assume we have a way to index searches.
    # To keep it simple and performant enough for a demo, we'll just check the 'property_requests' as that's the explicit feature requested.
    pass

def check_price_drop(property_id, new_data):
    new_price_str = new_data.get('price')
    if not new_price_str:
        return

    # Get old data
    old_doc = db.collection('properties').document(property_id).get()
    if not old_doc.exists:
        return
    
    old_data = old_doc.to_dict()
    old_price_str = old_data.get('price')
    
    if not old_price_str:
        return

    new_price = parse_price(new_price_str)
    old_price = parse_price(old_price_str)

    if new_price < old_price:
        # Price Dropped! Find users who favorited this property.
        # We need to query the 'users' collection, but favorites are subcollections.
        # Firestore Collection Group Query is best here.
        favorites_query = db.collection_group('favorites').stream()
        
        for fav in favorites_query:
            if fav.id == property_id:
                # This user favorited this property
                # fav.reference.parent.parent is the user document
                user_ref = fav.reference.parent.parent
                user_id = user_ref.id
                
                try:
                    user = auth.get_user(user_id)
                    if user.email:
                        notify_price_drop(user.email, old_data.get('title'), old_price_str, new_price_str, property_id)
                except:
                    pass
