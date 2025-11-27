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
    subject = f"Appointment Confirmed: {property_title}"
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
