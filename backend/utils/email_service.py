import logging

# Configure logging for emails
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EmailService")

import os
import requests
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv('RESEND_API_KEY')
EMAIL_FROM = os.getenv('EMAIL_FROM', 'onboarding@resend.dev')

from firebase_config import initialize_firebase

# Initialize Firebase for fetching templates
db, _ = initialize_firebase()

def get_email_template(template_name, default_subject, default_body):
    """
    Fetches email template from Firestore or returns default.
    """
    try:
        doc = db.collection('settings').document('email_templates').get()
        if doc.exists:
            data = doc.to_dict()
            if template_name in data:
                return data[template_name].get('subject', default_subject), data[template_name].get('body', default_body)
    except Exception as e:
        logger.error(f"Error fetching email template {template_name}: {e}")
    
    return default_subject, default_body

def send_email(to_email, subject, body):
    """
    Sends an email using the Resend API.
    """
    if not RESEND_API_KEY:
        logger.warning("RESEND_API_KEY not found. Falling back to mock email.")
        logger.info(f"--- MOCK EMAIL ---")
        logger.info(f"To: {to_email}")
        logger.info(f"Subject: {subject}")
        logger.info(f"Body: {body}")
        logger.info(f"------------------")
        return True

    try:
        url = "https://api.resend.com/emails"
        headers = {
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "from": EMAIL_FROM,
            "to": [to_email],
            "subject": subject,
            "html": body # Body is now expected to be HTML
        }

        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            logger.info(f"Email sent successfully to {to_email}")
            return True
        else:
            logger.error(f"Failed to send email: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"Exception sending email: {e}")
        return False

def notify_saved_search_match(user_email, search_name, property_title, property_id):
    default_subject = f"New Match for your search: {search_name}"
    default_body = f"""
    <p>Hello,</p>
    <p>A new property matching your saved search "<b>{search_name}</b>" has just been listed!</p>
    <p><b>Property:</b> {property_title}</p>
    <p><a href="http://localhost:5173/properties/{property_id}">View Property</a></p>
    <p>Best regards,<br>Krishna Properties Team</p>
    """
    
    subject, body = get_email_template('saved_search_match', default_subject, default_body)
    
    # Replace placeholders
    body = body.replace('{search_name}', search_name)\
               .replace('{property_title}', property_title)\
               .replace('{property_id}', property_id)\
               .replace('{property_link}', f"http://localhost:5173/properties/{property_id}")
               
    send_email(user_email, subject, body)

def notify_price_drop(user_email, property_title, old_price, new_price, property_id):
    default_subject = f"Price Drop Alert: {property_title}"
    default_body = f"""
    <p>Hello,</p>
    <p>Good news! The price for "<b>{property_title}</b>" has dropped.</p>
    <p><b>Old Price:</b> {old_price}<br>
    <b>New Price:</b> {new_price}</p>
    <p><a href="http://localhost:5173/properties/{property_id}">Check it out</a></p>
    <p>Best regards,<br>Krishna Properties Team</p>
    """
    
    subject, body = get_email_template('price_drop', default_subject, default_body)
    
    body = body.replace('{property_title}', property_title)\
               .replace('{old_price}', str(old_price))\
               .replace('{new_price}', str(new_price))\
               .replace('{property_id}', property_id)\
               .replace('{property_link}', f"http://localhost:5173/properties/{property_id}")

    send_email(user_email, subject, body)

def notify_appointment_confirmation(user_email, property_title, date, time):
    default_subject = f"Appointment Request Received: {property_title}"
    default_body = f"""
    <p>Hello,</p>
    <p>Your appointment request has been received.</p>
    <p><b>Property:</b> {property_title}<br>
    <b>Date:</b> {date}<br>
    <b>Time:</b> {time}</p>
    <p>We will contact you shortly to confirm the details.</p>
    <p>Best regards,<br>Krishna Properties Team</p>
    """
    
    subject, body = get_email_template('appointment_confirmation', default_subject, default_body)
    
    body = body.replace('{property_title}', property_title)\
               .replace('{date}', str(date))\
               .replace('{time}', str(time))

    send_email(user_email, subject, body)

def notify_appointment_status_change(user_email, property_title, date, time, status):
    default_subject = f"Appointment Update: {property_title}"
    default_body = f"""
    <p>Hello,</p>
    <p>Your appointment status has been updated to: <b>{status.upper()}</b>.</p>
    <p><b>Property:</b> {property_title}<br>
    <b>Date:</b> {date}<br>
    <b>Time:</b> {time}</p>
    <p>If you have any questions, please contact us.</p>
    <p>Best regards,<br>Krishna Properties Team</p>
    """
    
    subject, body = get_email_template('appointment_status_change', default_subject, default_body)
    
    body = body.replace('{property_title}', property_title)\
               .replace('{date}', str(date))\
               .replace('{time}', str(time))\
               .replace('{status}', status)

    send_email(user_email, subject, body)

def notify_appointment_reschedule(user_email, property_title, old_date, old_time, new_date, new_time):
    default_subject = f"Appointment Rescheduled: {property_title}"
    default_body = f"""
    <p>Hello,</p>
    <p>Your appointment has been rescheduled.</p>
    <p><b>Property:</b> {property_title}</p>
    <p><b>Previous Time:</b> {old_date} at {old_time}<br>
    <b>New Time:</b> {new_date} at {new_time}</p>
    <p>Please let us know if this new time works for you.</p>
    <p>Best regards,<br>Krishna Properties Team</p>
    """
    
    subject, body = get_email_template('appointment_reschedule', default_subject, default_body)
    
    body = body.replace('{property_title}', property_title)\
               .replace('{old_date}', str(old_date))\
               .replace('{old_time}', str(old_time))\
               .replace('{new_date}', str(new_date))\
               .replace('{new_time}', str(new_time))

    send_email(user_email, subject, body)

def notify_admin_new_lead(lead_type, data):
    admin_email = "admin@krishnaproperties.com" 
    default_subject = f"New Lead Alert: {lead_type}"
    
    details = ""
    for key, value in data.items():
        details += f"<b>{key}:</b> {value}<br>"

    default_body = f"""
    <h2>New {lead_type} Received</h2>
    <p>A new lead has been submitted on the website.</p>
    <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
        {details}
    </div>
    <p>Please check the admin dashboard for more details.</p>
    """
    
    # Admin notifications might not need dynamic templates, but we can support it
    subject, body = get_email_template('admin_new_lead', default_subject, default_body)
    
    body = body.replace('{lead_type}', lead_type)\
               .replace('{details}', details)

    send_email(EMAIL_FROM, subject, body)

def send_inquiry_auto_reply(user_email, name):
    default_subject = "We received your inquiry - Krishna Properties"
    default_body = f"""
    <p>Hello {name},</p>
    <p>Thank you for contacting Krishna Properties. We have received your message and our team will get back to you shortly.</p>
    <p>If your inquiry is urgent, please feel free to call us.</p>
    <p>Best regards,<br>Krishna Properties Team</p>
    """
    
    subject, body = get_email_template('inquiry_auto_reply', default_subject, default_body)
    
    body = body.replace('{name}', name)

    send_email(user_email, subject, body)

def send_request_auto_reply(user_email, name):
    default_subject = "Dream Home Request Received - Krishna Properties"
    default_body = f"""
    <p>Hello {name},</p>
    <p>Thank you for submitting your Dream Home request!</p>
    <p>We have received your preferences and our agents are already looking for properties that match your criteria. We will contact you as soon as we find something perfect for you.</p>
    <p>Best regards,<br>Krishna Properties Team</p>
    """
    
    subject, body = get_email_template('request_auto_reply', default_subject, default_body)
    
    body = body.replace('{name}', name)

    send_email(user_email, subject, body)
