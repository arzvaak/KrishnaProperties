from flask import Flask, jsonify
from flask_cors import CORS
from firebase_config import initialize_firebase

from routes.properties import properties_bp
from routes.users import users_bp
from routes.analytics import analytics_bp
from routes.appointments import appointments_bp
from routes.requests import requests_bp
from routes.inquiries import inquiries_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(properties_bp)
app.register_blueprint(users_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(appointments_bp)
app.register_blueprint(requests_bp)
app.register_blueprint(inquiries_bp)

# Initialize Firebase
try:
    db, bucket = initialize_firebase()
    print("Firebase initialized successfully")
except Exception as e:
    print(f"Error initializing Firebase: {e}")

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "Real Estate Backend"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
