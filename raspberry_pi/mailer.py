import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

class MailService:
    def __init__(self, mail_sender, mail_password, receiver_mail):

        self._mail_sender = mail_sender
        self._mail_password = mail_password
        self._receiver_mail = receiver_mail

    def send_alert(self, image_filename):

        alert_image = None
        with open(image_filename, 'rb') as f:
            alert_image = f.read()

        message = MIMEMultipart()
        message["Subject"] = "[ALERT] INTRUDER DETECTED"
        message["From"] = self._mail_sender
        message["To"] = self._receiver_mail

        text = MIMEText('Intruder detected on property.')
        message.attach(text)
        image = MIMEImage(alert_image)
        message.attach(image)
        print('sending mail!')
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465,
                              context=context) as server:
            server.login(self._mail_sender, self._mail_password)
            server.sendmail(self._mail_sender, self._receiver_mail,
                            message.as_string())