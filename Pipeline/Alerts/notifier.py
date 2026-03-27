import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

def send_email_alert(anomalies: list[dict],
                     sender: str,
                     password: str,
                     recipient: str) -> None:
    
    if not anomalies:
        logger.info("No anomalies detected, skipping email alert")
        return

    # step 1 - build subject and body
    subject = f"{len(anomalies)} Anomalies Detected in Log Analytics Engine!"
    
    body = f"Total Anomalies Detected: {len(anomalies)}\n\n"
    body += "=" * 50 + "\n"
    for a in anomalies:
        body += f"Service  : {a['Service Name']}\n"
        body += f"Level    : {a['Level']}\n"
        body += f"Status   : {a['Status_code']}\n"
        body += f"Z-Score  : {round(a['zscore'], 2)}\n"
        body += f"Message  : {a['message']}\n"
        body += f"Time     : {a['timestamp']}\n"
        body += "-" * 50 + "\n"

    # step 2 - create MIME message
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # step 3 - connect to Gmail SMTP and send
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
            logger.info(f"Alert email sent to {recipient}")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")