import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import random
import string
import os, dotenv
from datetime import datetime

dotenv.load_dotenv()

def get_password():
    if os.path.exists("../smtp.txt"):
            with open("../smtp.txt", 'r') as file:
                contents = file.read()
            return contents
    else:
        return os.getenv("SMTP_AUTH")
    
def generate_verify_code(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def verify_mail(receiver_email, username, verify_code, password=get_password()):
    # Static info:
    # login = "verify@autokafka.cz"
    login = "verify@autokafka.cz"
    smtp_server = "smtp.seznam.cz"
    smtp_port = 465
    sender_email = login
    subject = "Ověř svůj mail"
    body_template = f"""Klikni na tento odkaz, pokud chceš ověřit svůj účet <b>{username}</b><br>
            Pokud si o potvrzení nežádal, můžeš tento email ignorovat.<br>"""
    base_verify_url = "https://autokafka.cz/verify"

    status = {
        "sent_successfully": False,
        "error_message": "",
        "verifier_string": ""
    }
    verification_code = verify_code
    status["verifier_string"] = verification_code

    whole_verify_url = base_verify_url + "?code=" + verification_code
    body = body_template + f"""<a href="{whole_verify_url}">{whole_verify_url}</a>"""


    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(login, password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            status["sent_successfully"] = True
            # return status
    except Exception as e:
        status["error_message"] = str(e)
        # return status

    return status

def broadcast_mail(receiver_emails, file_path=None, password=get_password()):
    # Static info:
    login = "videa@autokafka.cz"
    smtp_server = "smtp.seznam.cz"
    smtp_port = 465
    sender_email = "videa@autokafka.cz"
    subject = f"Dějepis samostudium {datetime.now().strftime('%d.%m.')} - AutoKafka"
    body = f"""Dobrý den, zde zasílám odpovědi na otázky nejnovějšího samostudia. Přikládám soubor formátu Microsoft Word.<br><br>Pamatuj, že odpovědi jsem vygeneroval pomocí umělé inteligence, takže nemusí být správné. Zkontroluj si je před odevzdáním!<br><br>S pozdravem, AutoKafka."""

    status = {
        "sent_successfully": False,
        "error_message": "",
    }

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = "videa@autokafka.cz"
    # msg['Bcc'] = ",".join(receiver_emails)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    if file_path:
        attachment = open(file_path, "rb")
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)

        part.add_header("Content-Disposition",
        f"attachment; filename= {file_path.split('/')[-1]}")

        msg.attach(part)

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(login, password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_emails, text)
            status["sent_successfully"] = True
    except Exception as e:
        status["error_message"] = str(e)

    return status
