import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(to_email: str, subject: str, body: str, cc_email: str = None):
    try:
        load_dotenv()
        form_email = os.getenv("SENDER_EMAIL_USERNAME")
        password = os.getenv("SENDER_EMAIL_PASSWORD")

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, password)

        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        if cc_email:
            msg["Cc"] = cc_email

        msg.attach(MIMEText(body, "plain"))

        server.sendmail(from_email, [to_email] + ([cc_email] if cc_email else []), msg.as_string())

        server.quit()

    except Exception as e:
        logger.error(f"Failed to send email: {traceback.format_exc()}")
