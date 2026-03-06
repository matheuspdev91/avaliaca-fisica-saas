import os
import ssl
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import certifi


ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())

def send_email(subject, message, to_email):
    message = Mail(
        from_email='mpdev34@gmail.com',
        to_emails=to_email,
        subject=subject,
        plain_text_content=message,
    )

    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)

    return response.status_code