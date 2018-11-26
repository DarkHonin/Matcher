from app.framework import DataObject, Page
import uuid, flask
from datetime import datetime, timedelta

class RedeemPage(Page):
	def __init__(self):
		Page.__init__(self, {
			"/redeem/<token>:REDEEM_VIEW:GET" : self.view,
			"/redeem/<token>:REDEEM_ACTION:POST" : self.action,
		})

	def view(self, token):
		return flask.render_template("pages/index/redeem.html", token=token)

	def action(self, token):
		from app.framework.users import LoginUser, UserPage
		data = flask.request.json
		if not UserPage.LOGIN_VALIDATOR.validate(data):
			return  flask.jsonify({"status" : "NOJOY", "message" : UserPage.LOGIN_VALIDATOR.ERROR})
		print("Data logged")
		token = Token.get(Token, {"token" : token})
		if(not token):
			return flask.jsonify({"status" : UserPage.LOGIN_VALIDATOR.INVALID, "message" : "Your token is invalid"})
		user = token.resolve()
		if not LoginUser(user, data['password']):
			return flask.jsonify({"status" : "NOJOY", "message" : "Email/Password invalid"})
		token.delete()
		return flask.jsonify({"status" : UserPage.LOGIN_VALIDATOR.VALID, "action" : "redirect", "message" : "/user"})

class Token(DataObject):

	EXPIRE = 5

	def __init__(self, key : dict =None, callback : str =None):
		DataObject.__init__(self, "Tokens")
		self.date = datetime.now()
		from app import app
		if(app.config["TESTING"]):
			self.token =app.config["TESTING_TOKEN"]
		else:
			self.token = uuid.uuid1().hex
		self.key = key
		self.callback = callback


	def fieldKeys(self):
		return [
			"date"	,
			"key"	,
			"token" ,
			"callback" 
		]

	def isValid(self):
		now = datetime.now()
		age = now - self.date
		return age.days < self.EXPIRE

	def getKey(self):
		return list(self.key.keys())[0]

	def resolve(self):
		from app.framework import KEY_CLASSES
		cl = KEY_CLASSES[self.getKey()]
		id = self.key[self.getKey()]
		cl = cl.get(cl, {"_id" : id}, {"password" : 0})
		cl.__getattribute__(self.callback)(self)
		return cl