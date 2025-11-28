from flask import Blueprint, request, jsonify
from firebase_config import initialize_firebase
from firebase_admin import firestore, storage
import time
from routes.auth import verify_token

chat_bp = Blueprint('chat', __name__)
db, bucket = initialize_firebase()

# Rate limiting: Map of user_id -> [timestamps]
user_message_timestamps = {}
RATE_LIMIT_WINDOW = 60  # seconds
MAX_MESSAGES_PER_MINUTE = 10

def check_rate_limit(user_id):
    current_time = time.time()
    if user_id not in user_message_timestamps:
        user_message_timestamps[user_id] = []
    
    # Filter out timestamps older than the window
    user_message_timestamps[user_id] = [t for t in user_message_timestamps[user_id] if current_time - t < RATE_LIMIT_WINDOW]
    
    if len(user_message_timestamps[user_id]) >= MAX_MESSAGES_PER_MINUTE:
        return False
    
    user_message_timestamps[user_id].append(current_time)
    return True

@chat_bp.route('/api/chat/send', methods=['POST'])
@verify_token
def send_message():
    try:
        data = request.json
        sender_id = data.get('senderId')
        text = data.get('text')
        attachments = data.get('attachments', [])
        conversation_id = data.get('conversationId')
        recipient_id = data.get('recipientId') # 'admin' or user_uid

        if not sender_id or (not text and not attachments):
            return jsonify({"error": "Missing required fields"}), 400

        # Rate Limiting
        if not check_rate_limit(sender_id):
            return jsonify({"error": "Rate limit exceeded. Please wait a moment."}), 429

        # Create conversation if it doesn't exist
        if not conversation_id:
            # Check if conversation exists between these participants
            participants = sorted([sender_id, recipient_id])
            
            # Query for existing conversation (simplified for 1-on-1)
            # In a real app, you might query by participants array
            # For this use case (User <-> Admin), we can use a composite ID or query
            
            # Let's assume conversation ID is 'admin_<user_uid>' for simplicity if not provided
            # Or we create a new one.
            
            # Better approach: Query collection where participants array contains both
            # Firestore array-contains-any is limited.
            # For User-Admin, let's enforce conversation_id = user_uid (since it's 1:1 with admin)
            # If sender is admin, they must provide conversation_id (which is the user_uid)
            
            if recipient_id == 'admin':
                conversation_id = sender_id
            else:
                # Admin sending to user
                conversation_id = recipient_id
            
            # Check if doc exists, if not create
            conv_ref = db.collection('conversations').document(conversation_id)
            if not conv_ref.get().exists:
                conv_ref.set({
                    'participants': [sender_id, recipient_id],
                    'createdAt': firestore.SERVER_TIMESTAMP,
                    'unreadCount': {sender_id: 0, recipient_id: 0}
                })

        # Add Message
        message_data = {
            'senderId': sender_id,
            'text': text,
            'attachments': attachments,
            'timestamp': firestore.SERVER_TIMESTAMP,
            'read': False
        }
        
        # Add to sub-collection
        db.collection('conversations').document(conversation_id).collection('messages').add(message_data)
        
        # Update Conversation Metadata
        db.collection('conversations').document(conversation_id).update({
            'lastMessage': {
                'text': text if text else 'Attachment',
                'senderId': sender_id,
                'timestamp': firestore.SERVER_TIMESTAMP
            },
            'updatedAt': firestore.SERVER_TIMESTAMP,
            # Increment unread count for recipient
            f'unreadCount.{recipient_id}': firestore.Increment(1)
        })

        return jsonify({"message": "Message sent", "conversationId": conversation_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chat_bp.route('/api/chat/read', methods=['POST'])
@verify_token
def mark_read():
    try:
        data = request.json
        conversation_id = data.get('conversationId')
        user_id = data.get('userId') # The one reading the messages

        if not conversation_id or not user_id:
            return jsonify({"error": "Missing fields"}), 400

        # Reset unread count for this user
        db.collection('conversations').document(conversation_id).update({
            f'unreadCount.{user_id}': 0
        })
        
        return jsonify({"message": "Marked as read"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chat_bp.route('/api/chat/conversations/<user_id>', methods=['GET'])
@verify_token
def get_conversations(user_id):
    try:
        # Fetch conversations where user is a participant
        # Note: Firestore array-contains is needed
        docs = db.collection('conversations').where('participants', 'array_contains', user_id).order_by('updatedAt', direction=firestore.Query.DESCENDING).stream()
        
        conversations = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            conversations.append(data)
            
        return jsonify(conversations), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
