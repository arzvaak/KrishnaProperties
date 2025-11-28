from flask import Blueprint, jsonify
from firebase_config import initialize_firebase
from firebase_admin import firestore
from datetime import datetime, timedelta
from routes.auth import verify_admin

cleanup_bp = Blueprint('cleanup', __name__)
db, _ = initialize_firebase()

@cleanup_bp.route('/api/admin/cleanup', methods=['DELETE'])
@verify_admin
def cleanup_data():
    try:
        # 30 days ago
        cutoff_date = datetime.now() - timedelta(days=30)
        
        # 1. Analytics Aggregation & Cleanup
        events_ref = db.collection('events')
        # Query events older than cutoff
        # Note: Firestore requires an index for this query
        old_events = events_ref.where('timestamp', '<', cutoff_date).stream()
        
        aggregated_stats = {}
        batch = db.batch()
        count = 0
        deleted_count = 0
        
        for doc in old_events:
            data = doc.to_dict()
            event_type = data.get('type')
            timestamp = data.get('timestamp')
            
            if event_type and timestamp:
                # Convert timestamp to YYYY-MM
                # Timestamp might be a datetime object or Firestore Timestamp
                if hasattr(timestamp, 'date'):
                    month_key = timestamp.strftime('%Y-%m')
                else:
                    # Fallback if string or other format (should be datetime from Firestore)
                    continue
                
                # Aggregate
                key = f"{month_key}_{event_type}"
                aggregated_stats[key] = aggregated_stats.get(key, 0) + 1
            
            # Add to delete batch
            batch.delete(doc.reference)
            count += 1
            deleted_count += 1
            
            if count >= 400: # Commit batch every 400 items
                batch.commit()
                batch = db.batch()
                count = 0
                
        if count > 0:
            batch.commit()
            
        # Store Aggregated Stats
        for key, value in aggregated_stats.items():
            month, event_type = key.split('_', 1)
            stats_ref = db.collection('monthly_stats').document(month)
            # Use set with merge to update specific event type count
            # We need to increment, but since we are aggregating a batch of *deleted* events,
            # we can just increment the existing value by the count we found.
            stats_ref.set({
                event_type: firestore.Increment(value)
            }, merge=True)

        # 2. Cleanup Old Notifications
        notif_ref = db.collection('notifications')
        old_notifs = notif_ref.where('timestamp', '<', cutoff_date).stream()
        
        batch = db.batch()
        count = 0
        notif_deleted_count = 0
        
        for doc in old_notifs:
            batch.delete(doc.reference)
            count += 1
            notif_deleted_count += 1
            
            if count >= 400:
                batch.commit()
                batch = db.batch()
                count = 0
                
        if count > 0:
            batch.commit()

        return jsonify({
            "message": "Cleanup completed",
            "events_deleted": deleted_count,
            "notifications_deleted": notif_deleted_count,
            "aggregated_months": list(set(k.split('_')[0] for k in aggregated_stats.keys()))
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
