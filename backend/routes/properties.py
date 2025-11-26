from flask import Blueprint, request, jsonify
from firebase_config import initialize_firebase
from firebase_admin import firestore

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
        db.collection('properties').document(property_id).update(data)
        return jsonify({"message": "Property updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
