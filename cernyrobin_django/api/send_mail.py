import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string
import os

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
    login = "verify@cernyrob.in"
    smtp_server = "smtp.seznam.cz"
    smtp_port = 465
    sender_email = login
    subject = "Ověř svůj mail"
    body_template = f"""Klikni na tento odkaz, pokud chceš ověřit svůj účet <b>{username}</b><br>
            Pokud si o potvrzení nežádal, můžeš tento email ignorovat.<br>"""
    base_verify_url = "https://cernyrob.in/verify"

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
    print(password)
    print(status)

    return status