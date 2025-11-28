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
            "html": body.replace('\n', '<br>')  # Simple text to HTML conversion
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
    subject = f"New Match for your search: {search_name}"
    body = f"""
    Hello,

    A new property matching your saved search "{search_name}" has just been listed!

    Property: {property_title}
    Link: http://localhost:5173/properties/{property_id}

    Best regards,
    Krishna Properties Team
    """
    send_email(user_email, subject, body)

def notify_price_drop(user_email, property_title, old_price, new_price, property_id):
    subject = f"Price Drop Alert: {property_title}"
    body = f"""
    Hello,

    Good news! The price for "{property_title}" has dropped.

    Old Price: {old_price}
    New Price: {new_price}

    Check it out: http://localhost:5173/properties/{property_id}

    Best regards,
    Krishna Properties Team
    """
    send_email(user_email, subject, body)

def notify_appointment_confirmation(user_email, property_title, date, time):
    subject = f"Appointment Request Received: {property_title}"
    body = f"""
    Hello,

    Your appointment request has been received.

    Property: {property_title}
    Date: {date}
    Time: {time}

    We will contact you shortly to confirm the details.

    Best regards,
    Krishna Properties Team
    """
    send_email(user_email, subject, body)

def notify_appointment_status_change(user_email, property_title, date, time, status):
    subject = f"Appointment Update: {property_title}"
    body = f"""
    Hello,

    Your appointment status has been updated to: <b>{status.upper()}</b>.

    Property: {property_title}
    Date: {date}
    Time: {time}

    If you have any questions, please contact us.

    Best regards,
    Krishna Properties Team
    """
    send_email(user_email, subject, body)

def notify_appointment_reschedule(user_email, property_title, old_date, old_time, new_date, new_time):
    subject = f"Appointment Rescheduled: {property_title}"
    body = f"""
    Hello,

    Your appointment has been rescheduled.

    Property: {property_title}
    
    <b>Previous Time:</b> {old_date} at {old_time}
    <b>New Time:</b> {new_date} at {new_time}

    Please let us know if this new time works for you.

    Best regards,
    Krishna Properties Team
    """
    send_email(user_email, subject, body)

def notify_admin_new_lead(lead_type, data):
    """
    Notifies the admin about a new lead.
    lead_type: 'Appointment', 'Property Request', 'Inquiry'
    data: Dictionary containing lead details
    """
    # In a real app, this would be the admin's email
    admin_email = "admin@krishnaproperties.com" 
    subject = f"New Lead Alert: {lead_type}"
    
    details = ""
    for key, value in data.items():
        details += f"<b>{key}:</b> {value}<br>"

    body = f"""
    <h2>New {lead_type} Received</h2>
    <p>A new lead has been submitted on the website.</p>
    <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
        {details}
    </div>
    <p>Please check the admin dashboard for more details.</p>
    """
    # For now, we'll just log it or send to a dev email if configured
    # In production, you'd send this to the actual admin
    send_email(EMAIL_FROM, subject, body) # Sending to sender for testing purposes

def send_inquiry_auto_reply(user_email, name):
    subject = "We received your inquiry - Krishna Properties"
    body = f"""
    Hello {name},

    Thank you for contacting Krishna Properties. We have received your message and our team will get back to you shortly.

    If your inquiry is urgent, please feel free to call us at +91 98765 43210.

    Best regards,
    Krishna Properties Team
    """
    send_email(user_email, subject, body)

def send_request_auto_reply(user_email, name):
    subject = "Dream Home Request Received - Krishna Properties"
    body = f"""
    Hello {name},

    Thank you for submitting your Dream Home request! 
    
    We have received your preferences and our agents are already looking for properties that match your criteria. We will contact you as soon as we find something perfect for you.

    Best regards,
    Krishna Properties Team
    """
    send_email(user_email, subject, body)
