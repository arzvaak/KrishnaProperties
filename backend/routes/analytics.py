from flask import Blueprint, request, jsonify
from firebase_config import initialize_firebase
from firebase_admin import firestore
from datetime import datetime
from routes.auth import verify_admin

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
            'user_id': data.get('user_id'), # Track who triggered the event
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
@verify_admin
def get_dashboard_stats():
    try:
        # 1. General Stats
        stats_doc = db.collection('stats').document('general').get()
        stats = stats_doc.to_dict() or {'site_views': 0, 'total_contacts': 0}
        
        # 2. Total Properties
        props_ref = db.collection('properties')
        total_properties = len(list(props_ref.stream()))
        
        # 3. Total Users (Approximate)
        users_ref = db.collection('users')
        total_users = len(list(users_ref.stream()))

        # 4. Total Leads & Funnel
        inquiries = list(db.collection('inquiries').stream())
        requests = list(db.collection('property_requests').stream())
        total_leads = len(inquiries) + len(requests)
        
        funnel = {
            'new': 0,
            'contacted': 0,
            'qualified': 0,
            'converted': 0,
            'lost': 0
        }
        
        for doc in inquiries + requests:
            data = doc.to_dict()
            status = data.get('status', 'new').lower()
            if status in funnel:
                funnel[status] += 1
            else:
                funnel['new'] += 1 # Default to new if unknown

        # 5. Most Viewed Properties (Top 5)
        # Note: This requires 'views' field on properties. 
        # Ideally we index this. For now, we sort in memory if dataset is small, 
        # or use order_by if indexed.
        top_props_query = props_ref.order_by('views', direction=firestore.Query.DESCENDING).limit(5).stream()
        most_viewed = []
        for doc in top_props_query:
            d = doc.to_dict()
            most_viewed.append({
                'id': doc.id,
                'title': d.get('title', 'Unknown'),
                'views': d.get('views', 0)
            })

        # 6. Traffic Stats (Last 30 Days)
        # We need to aggregate 'site_view' events by date.
        # This is expensive to do on-the-fly from raw events.
        # Ideally, we should have a scheduled job that aggregates this into a 'daily_stats' collection.
        # For this MVP, we will simulate or fetch from a 'daily_stats' collection if we had one.
        # Let's aggregate from 'events' for now (limit to recent 1000 to avoid timeout)
        
        traffic_stats = {}
        events_query = db.collection('events').where('type', '==', 'site_view') \
            .order_by('timestamp', direction=firestore.Query.DESCENDING).limit(500).stream()
            
        for doc in events_query:
            data = doc.to_dict()
            ts = data.get('timestamp')
            if ts:
                date_str = ts.strftime('%Y-%m-%d')
                traffic_stats[date_str] = traffic_stats.get(date_str, 0) + 1
                
        # Fill in missing dates for the last 7 days at least
        sorted_traffic = []
        # (Simplified: just returning what we found, frontend can fill gaps or show available data)
        for date, count in sorted(traffic_stats.items()):
            sorted_traffic.append({'date': date, 'count': count})

        # 7. Recent Activity
        events_ref = db.collection('events').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(10)
        recent_events = []
        for doc in events_ref.stream():
            data = doc.to_dict()
            if data.get('timestamp'):
                data['timestamp'] = data['timestamp'].isoformat()
            recent_events.append(data)
            
        return jsonify({
            "site_views": stats.get('site_views', 0),
            "total_contacts": stats.get('total_contacts', 0),
            "total_properties": total_properties,
            "total_users": total_users,
            "total_leads": total_leads,
            "funnel": funnel,
            "most_viewed_properties": most_viewed,
            "traffic_stats": sorted_traffic,
            "recent_events": recent_events
        }), 200
    except Exception as e:
        print(f"Analytics Error: {e}")
        return jsonify({"error": str(e)}), 500

@analytics_bp.route('/api/analytics/public-stats', methods=['GET'])
def get_public_stats():
    try:
        # 1. Total Properties
        props_ref = db.collection('properties')
        total_properties = len(list(props_ref.stream()))
        
        # 2. Total Clients (Mocked base + real count)
        users_ref = db.collection('users')
        total_users = 2000 + len(list(users_ref.stream()))
        
        # 3. Cities (Count unique cities)
        # This is expensive if we iterate all. For now, let's mock or estimate.
        # Ideally, we maintain a 'cities' collection or aggregate.
        # Let's just return a static number + distinct cities count if small.
        cities = set()
        for doc in props_ref.stream():
            city = doc.to_dict().get('location', {}).get('city')
            if city:
                cities.add(city)
        total_cities = 10 + len(cities) # Mock base

        return jsonify({
            "properties": total_properties,
            "clients": total_users,
            "cities": total_cities,
            "support": "24/7"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
