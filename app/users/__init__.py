from app.users.User_class import User
from app.users.password import Password
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

import flask
import uuid

from app.token import AddKeyClass

AddKeyClass("Users", User)

def RegisterUser(user, password):
	user.log_fields()
	if not user.save():
		return False
	print("user created")
	password = Password(generate_password_hash(password), user.id)
	password.save()
	print("password created")
	from flask_mail import Message
	from app import Mailer
	from app.token import Token

	token = Token({"Users" : user.id}, "activate")
	token.save()
	msg = Message("Activate the shrines",recipients=[user.email], html=flask.render_template("pages/email/activateEmail.html", token=token.token))
	Mailer.send(msg)
	return True

def LookupUser(uname):
	user = User.get(User, {"uname" : uname})
	return user

def verifyLogin(user : User, password, resp={}):
	if not user:
		resp['error'] = {"status" : "NOJOY", "message" : "Email/Password invalid"}
		return False
	user.log_fields()
	if not check_password_hash(user.password['value'], password):
		resp['error'] = {"status" : "NOJOY", "message" : "Email/Password invalid"}
		return False
	return True

def LoginUser(user : User, password):
	if not user:
		return False
	stored_password = Password.get(Password, {'user' : user.id})
	if not check_password_hash(stored_password.hash, password): 
		return False
	user.lastLogin = datetime.now()
	flask.session['user'] = user.uid
	user.save()
	return True

def logout():
	if "user" in flask.session:
		del flask.session['user']
	return flask.redirect("/")
