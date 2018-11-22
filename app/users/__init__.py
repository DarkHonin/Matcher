from app.users.User_class import User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import flask
import uuid

from app.token import AddKeyClass

AddKeyClass("Users", User)

Users = {}

def RegisterUser(data, resp={}):
	user = User()
	user.parse_dbo(data)
	user.log_fields()
	user.s("password", generate_password_hash(data['password']))
	if not user.save():
		resp["error"] = user.ERROR
		return False
	from flask_mail import Message
	from app import Mailer
	from app.token import Token

	token = Token()
	token.s('key', {"Users" : user.id})
	token.s("callback", "activate")
	token.save()
	msg = Message("Activate the shrines",recipients=[data['email']], html=flask.render_template("pages/email/activateEmail.html", token=token.g('token')))
	Mailer.send(msg)
	return True

def verifyLogin(user : User, password, resp={}):
	if not user:
		resp['error'] = {"status" : "NOJOY", "message" : "Email/Password invalid"}
		return False
	user.log_fields()
	if not check_password_hash(user.password['value'], password):
		resp['error'] = {"status" : "NOJOY", "message" : "Email/Password invalid"}
		return False
	return True

def LoginUser(data, resp={}):
	user = User.get(User, {"email" : data['email']})
	verifyLogin(user,data['password'], resp)
	sesh = uuid.uuid4().hex
	Users[sesh] = user
	user.sessionID['value'] = sesh
	user.save()
	return True