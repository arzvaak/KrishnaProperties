from flask import Blueprint, request, jsonify
from firebase_config import initialize_firebase
from firebase_admin import firestore
from datetime import datetime

leads_bp = Blueprint('leads', __name__)
db, _ = initialize_firebase()

def normalize_lead(doc, lead_type):
    data = doc.to_dict()
    data['id'] = doc.id
    data['type'] = lead_type
    
    # Normalize timestamp
    if lead_type == 'inquiry':
        data['createdAt'] = data.get('timestamp')
        data['title'] = data.get('subject') or f"Inquiry from {data.get('name')}"
    elif lead_type == 'request':
        data['createdAt'] = data.get('created_at')
        criteria = data.get('criteria', {})
        data['title'] = f"Request: {criteria.get('type', 'Property')} in {criteria.get('location', 'Anywhere')}"
        data['name'] = "User " + (data.get('user_id')[:6] if data.get('user_id') else "Guest")

    # Ensure status exists
    if 'status' not in data:
        data['status'] = 'new'
        
    # Ensure source exists
    if 'source' not in data:
        data['source'] = 'Website'
        
    return data

@leads_bp.route('/api/admin/leads', methods=['GET'])
def get_all_leads():
    try:
        # Fetch Inquiries
        inquiries_ref = db.collection('inquiries')
        inquiries_docs = inquiries_ref.stream()
        
        # Fetch Property Requests
        requests_ref = db.collection('property_requests')
        requests_docs = requests_ref.stream()
        
        leads = []
        
        for doc in inquiries_docs:
            leads.append(normalize_lead(doc, 'inquiry'))
            
        for doc in requests_docs:
            leads.append(normalize_lead(doc, 'request'))
            
        # Sort by createdAt descending
        leads.sort(key=lambda x: x.get('createdAt', datetime.min).timestamp() if x.get('createdAt') else 0, reverse=True)
            
        return jsonify(leads), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@leads_bp.route('/api/admin/leads/export', methods=['GET'])
def export_leads():
    try:
        import csv
        import io
        from flask import make_response

        # Fetch all leads (reuse logic or call internal function)
        inquiries_docs = db.collection('inquiries').stream()
        requests_docs = db.collection('property_requests').stream()
        
        leads = []
        for doc in inquiries_docs:
            leads.append(normalize_lead(doc, 'inquiry'))
        for doc in requests_docs:
            leads.append(normalize_lead(doc, 'request'))
            
        leads.sort(key=lambda x: x.get('createdAt', datetime.min).timestamp() if x.get('createdAt') else 0, reverse=True)

        # Create CSV
        si = io.StringIO()
        cw = csv.writer(si)
        
        # Header
        cw.writerow(['ID', 'Type', 'Name', 'Email', 'Phone', 'Status', 'Source', 'Date', 'Title/Property'])
        
        # Rows
        for lead in leads:
            cw.writerow([
                lead.get('id', ''),
                lead.get('type', ''),
                lead.get('name', ''),
                lead.get('email', ''),
                lead.get('phone', ''),
                lead.get('status', ''),
                lead.get('source', 'Website'),
                lead.get('createdAt', ''),
                lead.get('title', '') or lead.get('property_title', '')
            ])
            
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=leads_export.csv"
        output.headers["Content-type"] = "text/csv"
        return output
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@leads_bp.route('/api/admin/leads/<lead_type>/<lead_id>', methods=['GET'])
def get_lead_details(lead_type, lead_id):
    try:
        collection_name = 'inquiries' if lead_type == 'inquiry' else 'property_requests'
        doc = db.collection(collection_name).document(lead_id).get()
        
        if not doc.exists:
            return jsonify({"error": "Lead not found"}), 404
            
        return jsonify(normalize_lead(doc, lead_type)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@leads_bp.route('/api/admin/leads/<lead_type>/<lead_id>', methods=['PATCH'])
def update_lead_status(lead_type, lead_id):
    try:
        data = request.json
        collection_name = 'inquiries' if lead_type == 'inquiry' else 'property_requests'
        
        ref = db.collection(collection_name).document(lead_id)
        
        update_data = {}
        if 'status' in data:
            update_data['status'] = data['status']
        if 'notes' in data:
            # This replaces notes, for appending use the notes endpoint
            update_data['notes'] = data['notes']
            
        ref.update(update_data)
        
        return jsonify({"message": "Lead updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@leads_bp.route('/api/admin/leads/<lead_type>/<lead_id>/notes', methods=['POST'])
def add_lead_note(lead_type, lead_id):
    try:
        data = request.json
        note_text = data.get('text')
        author = data.get('author', 'Admin')
        
        if not note_text:
            return jsonify({"error": "Note text is required"}), 400
            
        collection_name = 'inquiries' if lead_type == 'inquiry' else 'property_requests'
        ref = db.collection(collection_name).document(lead_id)
        
        note = {
            'text': note_text,
            'author': author,
            'timestamp': datetime.now().isoformat()
        }
        
        # Atomically add note to array
        ref.update({
            'notes': firestore.ArrayUnion([note])
        })
        
        return jsonify(note), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
