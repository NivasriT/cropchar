import smtplib
from email.mime.text import MIMEText
from backend.core.config import settings

def send_alert_email(to_email: str, field_id: str, acq_date: str) -> None:
    subject = f"Unauthorized burn detected — Field {field_id}"
    body = (
        f"An unauthorized crop residue burn was detected.\n\n"
        f"Field ID: {field_id}\n"
        f"Detection Date: {acq_date}\n\n"
        f"— CropChar Monitoring System"
    )
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_ADDRESS
    msg["To"] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(settings.EMAIL_ADDRESS, settings.EMAIL_APP_PASSWORD)
            server.send_message(msg)
    except smtplib.SMTPAuthenticationError:
        raise RuntimeError("Email auth failed — check EMAIL_ADDRESS / EMAIL_APP_PASSWORD in .env")
    except Exception as e:
        raise RuntimeError(f"Failed to send alert email: {e}")