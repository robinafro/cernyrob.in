import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string




def generate_verify_code(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


def verify_mail(receiver_email, username, password):
    #Static info:
    login = "verify@cernyrob.in"
    smtp_server = "smtp.seznam.cz"
    smtp_port = 465
    sender_email = login
    subject = "Ověř svůj mail mail"
    body_template = f"""Klikni na tento odkaz, pokud chceš ověřit svůj účet {username}<br>
            Pokud si o potvrzení nežádal, můžeš tenhle mail ignorovat.<br>"""
    base_verify_url = "https://cernyrob.in/verify_email/"

    verification_code = generate_verify_code(16)

    whole_verify_url = base_verify_url + "?code=" + verification_code
    body = body_template + whole_verify_url
    
    status = { 
        "sent_successfully" : False,
        "error_message" : "",
        "verifier_string" : ""
    }

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(login, password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            status.sent_successfully = True
            return status
    except Exception as e:
        status.error_message = str(e)
        return status

# Example usage
receiver_email = "adam.vi.2023@skola.ssps.cz"


password = "yourpassword"#Get from .env
cernyrobin_username = "StuckInVim"

response = verify_mail(receiver_email, cernyrobin_username, password,)
print(response)
