from users.tokens.token import Token
from api import APIException

class InvalidEmailMessage(APIException):
    pass

def redeemToken(tokenHash):
    token = Token.get({"token" : tokenHash})
    if not token:
        raise APIException(message="The token provided is invalid")
    subject = token.subject
    if not subject:
        print(subject)
        return
    action = getattr(subject, token.action)
    action()
    token.delete()

def sendTokenEmail(email, token):
    from flask_mail import Message
    from flask import render_template
    from app import MAILER
    from smtplib import SMTPRecipientsRefused
    from socket import gaierror
    from systems.exceptions import SystemException
    msg = Message("The keys to Valhalla",recipients=[email], html=render_template("users/activateEmail.html", token=token.token))
    try:
        MAILER.send(msg)
    except SMTPRecipientsRefused:
        raise InvalidEmailMessage(message="Your email was invalid")
    except gaierror:
        from app import APP
        if not (APP.config["IGNORE_SMTP_CONNECT_ERROR"]):
            raise InvalidEmailMessage(message="Could not send your activation email")
    token.save()