import smtplib
from email.mime.text import MIMEText

SMTP_HOST = "localhost"
SMTP_PORT = 1025
FROM_EMAIL = "admin@college.com"

def send_email(to_email, subject, body, html_body=None):

    if html_body:
        msg = MIMEText(html_body, 'html')
    else:
        msg = MIMEText(body, 'plain')

    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.send_message(msg)
            print(f" Successfully sent email to {to_email}")
            return True
    except Exception as e:
        print(f"Failed to send email to {to_email}. Error: {e}")
        return False
