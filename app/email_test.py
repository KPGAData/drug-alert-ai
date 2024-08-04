import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import os
from dotenv import load_dotenv

# Initialize
load_dotenv()

SMTP_FROM = os.environ["SMTP_FROM"]
SMTP_TO = os.environ["SMTP_TO"]
SMTP_SERVER = os.environ["SMTP_SERVER"]
SMTP_PORT = os.environ["SMTP_PORT"]
SMTP_USER = os.environ["SMTP_USER"]
SMTP_PASS = os.environ["SMTP_PASS"]

# Create the email message
msg = MIMEMultipart('alternative')
msg['Subject'] = f"Latest drug information"
msg['From'] = SMTP_FROM
msg['To'] = SMTP_TO

html_content = """
    <html><body>Hello</body></html>
"""
# Attach the HTML content
html_part = MIMEText(html_content, 'html')
msg.attach(html_part)

# Send the email
try:
    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
    print("Email sent successfully")
except Exception as e:
    print(f"Error sending email: {e}")