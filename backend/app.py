from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import sentry_sdk
from firebase_config import initialize_firebase

import os

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

from routes.properties import properties_bp
from routes.users import users_bp
from routes.analytics import analytics_bp
from routes.appointments import appointments_bp
from routes.requests import requests_bp
from routes.inquiries import inquiries_bp
from routes.chat import chat_bp
from routes.leads import leads_bp
from routes.blogs import blogs_bp
from routes.cleanup import cleanup_bp
from routes.notifications import notifications_bp

app = Flask(__name__)
CORS(app)

# Security Headers
Talisman(app, force_https=False, content_security_policy=None)

# Rate Limiting
limiter = Limiter(
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
