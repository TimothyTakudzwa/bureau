from flask_mail import Mail, Message

from . import app, mail


def send_email(to, subject, template):
    msg = Message(subject,recipients=[to],html=template,sender=app.config['MAIL_USERNAME'])
    mail.send(msg)