from systems.tokens.token import Token

def redeemToken(tokenHash):
    from systems.exceptions import InvalidTokenError
    token = Token.get({"token" : tokenHash})
    if not token:
        raise InvalidTokenError("The token provided is invalid")
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
    from app import Mailer
    from smtplib import SMTPRecipientsRefused
    from systems.exceptions import SystemException
    msg = Message("The keys to Valhalla",recipients=[email], html=render_template("pages/email/activateEmail.html", token=token.token))
    try:
        Mailer.send(msg)
    except SMTPRecipientsRefused:
        raise SystemException("Your email is invalid", SystemException.FIELD_ERROR)