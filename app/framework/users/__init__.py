from app.framework.users.User_class import User
from app.framework.users.Page import UserPage
from app.framework.users.password import Password
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from geventwebsocket.websocket import WebSocket
from app.framework.users import SocketDispatch

import flask
import uuid

from app.framework import AddKeyClass

AddKeyClass("Users", User)

def RegisterUser(user, password):
	user.log_fields()
	if not user.save():
		return False
	print("user created")
	user.password = password
	print("password created")
	sendActivationEmail(user)
	return True

def sendActivationEmail(user):
	from flask_mail import Message
	from app import Mailer
	from app.framework import Token

	token = Token({"Users" : user.id}, "activate")
	token.save()
	msg = Message("Activate the shrines",recipients=[user.email], html=flask.render_template("pages/email/activateEmail.html", token=token.token))
	Mailer.send(msg)

def LookupUser(uname):
	user = User.get(User, {"uname" : uname})
	return user

def GetCurrentUser():
	if not 'user' in flask.session:
		return False
	return User.get(User, {"uid" : flask.session['user']})

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