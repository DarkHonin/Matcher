from app.users import User
from .dbo import Token
from .api import APIInvalidEmail, APICouldNotConnectToMailServer

def create_token(user : User, callback : str):
	token = Token(callback, user._id)
	token.save()
	mail_token(user.email, token)

def redeem_token(token):
	pass

def mail_token(email, token):
	from flask_mail import Message
	from flask import render_template
	from app import EMAIL_CLIENT
	from smtplib import SMTPRecipientsRefused
	from socket import gaierror
	msg = Message("The keys to Valhalla",recipients=[email], html=render_template("users/activateEmail.html", token=token.token))
	try:
		EMAIL_CLIENT.send(msg)
		print("Token email sent to :", email)
	except SMTPRecipientsRefused:
		raise APIInvalidEmail()
	except gaierror:
		from app import APP
		if not (APP.config["IGNORE_SMTP_CONNECT_ERROR"]):
			raise APICouldNotConnectToMailServer()