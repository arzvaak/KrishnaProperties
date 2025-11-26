from flask import Blueprint, request, jsonify
from firebase_config import initialize_firebase
from firebase_admin import firestore
from datetime import datetime

analytics_bp = Blueprint('analytics', __name__)
db, bucket = initialize_firebase()

@analytics_bp.route('/api/analytics/track', methods=['POST'])
def track_event():
    try:
        data = request.json
        event_type = data.get('type') # 'site_view', 'property_view', 'contact', 'like'
        property_id = data.get('property_id')
        metadata = data.get('metadata', {})
        
        event_data = {
            'type': event_type,
            'timestamp': firestore.SERVER_TIMESTAMP,
            'property_id': property_id,
            'metadata': metadata
        }
        
        # Add to 'events' collection
        db.collection('events').add(event_data)
        
        # Update aggregate counters (optional, for faster dashboard loading)
        if event_type == 'site_view':
            stats_ref = db.collection('stats').document('general')
            stats_ref.set({'site_views': firestore.Increment(1)}, merge=True)
            
        elif event_type == 'property_view' and property_id:
            prop_ref = db.collection('properties').document(property_id)
            prop_ref.update({'views': firestore.Increment(1)})
            
        elif event_type == 'contact':
            stats_ref = db.collection('stats').document('general')
            stats_ref.set({'total_contacts': firestore.Increment(1)}, merge=True)
            
        return jsonify({"message": "Event tracked"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@analytics_bp.route('/api/analytics/dashboard', methods=['GET'])
def get_dashboard_stats():
    try:
        # Get general stats
        stats_doc = db.collection('stats').document('general').get()
        stats = stats_doc.to_dict() or {'site_views': 0, 'total_contacts': 0}
        
        # Get total properties
        props_ref = db.collection('properties')
        total_properties = len(list(props_ref.stream())) # Note: In production, use aggregation query
        
        # Get recent events
        events_ref = db.collection('events').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(10)
        recent_events = []
        for doc in events_ref.stream():
            data = doc.to_dict()
            # Convert timestamp to string
            if data.get('timestamp'):
                data['timestamp'] = data['timestamp'].isoformat()
            recent_events.append(data)
            
        return jsonify({
            "site_views": stats.get('site_views', 0),
            "total_contacts": stats.get('total_contacts', 0),
            "total_properties": total_properties,
            "recent_events": recent_events
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
