import os
import smtplib
from langchain.tools import tool
import logging
from logging import getLogger
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app_logger = getLogger(__name__)
app_logger.info("TOOLS")


#@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Envoie un email.

    Args:
        to: Destinataire
        subject: sujet du mail
        body: text du mail
    """
    app_logger.info("send_email")


    msg = MIMEMultipart()
    msg["From"] = os.getenv('DEFAULT_EMAIL')
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, 'plain'))

    # SMTP local MailHog
    try:
        with smtplib.SMTP(os.getenv('SMTP_ADRESS'), os.getenv('SMTP_PORT')) as smtp:
            smtp.send_message(msg)
        app_logger.info("MAILHOG")
        return f"Email sent to {to} (via MailHog)"
    except Exception as e:
        return f"Failed to send email: {e}"


@tool
def create_calendar_event(title: str, date: str, time: str) -> str:
    """Crée un événement (simulé)"""
    app_logger.info("create_calendar_event")
    return f"Événement simulé créé : '{title}' le {date} à {time}"
