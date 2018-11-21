from app.users.User_class import User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from app.token import AddKeyClass

AddKeyClass("Users", User)

def RegisterUser(data, resp={}):
	user = User()
	user.parse_dbo(data)
	user.log_fields()
	user.password['value'] = generate_password_hash(data['password'])
	if not user.save():
		resp["error"] = user.ERROR
		return False
	from flask_mail import Message
	from app import Mailer
	from app.token import Token

	token = Token({"Users" : user.id}, "activate")
	token.save()
	msg = Message("Hello",
				recipients=[data['email']], body=token.token['value'])
	Mailer.send(msg)
	return True

def LoginUser(data, resp={}):
	user = User.get(User, {"email" : data['email']}, {"active" : 1, "password" : 1})
	if not user:
		resp['error'] = {"status" : "NOJOY", "message" : "Email/Password invalid"}
		return False
	user.log_fields()
	if(not user.active['value']):
		resp['error'] = {"status" : "NOJOY", "message" : "Your account is not active yet, please check your email"}
		return False
	if not check_password_hash(user.password['value'], data['password']):
		resp['error'] = {"status" : "NOJOY", "message" : "Email/Password invalid"}
		return False
	user.lastLogin['value'] = datetime.now()
	user.save()
	return True