import smtplib
import ssl
import json
import os
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()
EMAIL = json.loads(os.getenv("EMAIL"))

def sendmail(subject, message):
    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtpout.secureserver.net", port, context=context) as server:
        server.login(EMAIL['sender'], EMAIL['password'])
        
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = EMAIL['sender']
        message["To"] = EMAIL['receiver']

        server.sendmail(
            EMAIL['sender'], EMAIL['receiver'], message.as_string()
        )
