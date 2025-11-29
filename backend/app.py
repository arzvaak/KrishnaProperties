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
# Restrict CORS to frontend origin
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "https://krishna-properties-f396d.web.app"]}})

# Security Headers
csp = {
    'default-src': '\'self\'',
    'script-src': '\'self\' \'unsafe-inline\' https://apis.google.com',
    'connect-src': '\'self\' https://identitytoolkit.googleapis.com https://securetoken.googleapis.com https://firestore.googleapis.com',
    'img-src': '\'self\' data: https://firebasestorage.googleapis.com',
    'style-src': '\'self\' \'unsafe-inline\''
}
# Force HTTPS in production (when debug is False)
force_https = os.getenv('FORCE_HTTPS', 'False') == 'True'
Talisman(app, force_https=force_https, content_security_policy=csp)

from extensions import limiter

# Rate Limiting
limiter.init_app(app)

# Security Headers
Talisman(app, force_https=False, content_security_policy=None)

# Rate Limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

app.register_blueprint(properties_bp)
app.register_blueprint(users_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(appointments_bp)
app.register_blueprint(requests_bp)
app.register_blueprint(inquiries_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(leads_bp)
app.register_blueprint(blogs_bp)
app.register_blueprint(cleanup_bp)
app.register_blueprint(notifications_bp, url_prefix='/api/notifications')

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
    app.run(debug=os.getenv('FLASK_DEBUG', 'False') == 'True', port=5000)
