from app.framework import Page
from app.framework.users import User
from app.framework import Token, Page, JsonResponce
from app.framework.validator import *
import uuid
import flask

class UserPage(Page):

	LOGIN_VALIDATOR = Validator(
        [
            PASSWORD_FIELD,
            UNAME_FIELD,
            Field("g-recaptcha-response", {"Captvha failed" : Validator.checkCaptcha}, True, "Captcha"),
        ]  
    )

	REGISTER_VALIDATOR = Validator(
            [
                EMAIL_FIELD,
                PASSWORD_FIELD,
                Field("fname", {"Not a valid first name" : Validator.isValidName}, True, "First name"),
                Field("lname", {"Not a valid last name" : Validator.isValidName}, True, "Lirst name"),
                UNAME_FIELD,
                Field("g-recaptcha-response", {"Captvha failed" : Validator.checkCaptcha}, True, "Captcha")
            ]  
        )

	LOGGED_USERS = {}

	def __init__(self):
		 Page.__init__(self, {
            "/:INDEX:GET" 								: self.showLoginPage,
            "/login:LOGIN:GET" 							: self.showLoginPage,
            "/login:LOGIN_ACTION:POST" 					: self.loginUser,
            "/register:REGISTER:GET" 					: self.showRegisterPage,
            "/register:REGISTER_ACTION:POST" 			: self.registerUser,
			"/home:HOME_VIEW:GET" 						: self.showHomePage,
			"/logut:LOGOUT:GET"							: self.logout,
			"/userSettings/<part>:SETTING_FIELD:GET"	: self.getFieldHTML,
			"/userSettings/<part>:SETTING_SAVE:POST"	: self.saveField
        })

	def getFieldHTML(self, part):
		from app.framework.users import GetCurrentUser
		if not self.isUserLoggedIn():
			return flask.jsonify({"status" : "NOJOY", "message" : "HA! Youre not logged in!"})
		field = User.GLOBAL_VALIDATOR.fieldFor(part)
		if not field:
			return flask.jsonify({"status" : "NOJOY", "message" : "No field with key "+part})
		value = GetCurrentUser().__getattribute__(part)
		return flask.jsonify({"status" : "JOY", "data" : flask.render_template(field.template(), field=field, value=value)})

	def saveField(self, part):
		if not self.isUserLoggedIn():
			return flask.jsonify({"status" : "NOJOY", "message" : "HA! Youre not logged in!"})
		data = flask.request.json
		field = User.GLOBAL_VALIDATOR.fieldFor(part)
		if( not field.validate(data['value'])):
			return  flask.jsonify({"status" : "NOJOY", "message" : field.ERROR})
		user = self.getCurrentUser()
		if not ('token' in data):
			return flask.jsonify({"status" : "NOJOY", "message" : "No token man!"})
		if not self.LOGGED_USERS[user.uid]['SessionID'] == data['token']:
			return flask.jsonify({"status" : "NOJOY", "message" : "Invalid token!"})
		if(part is "email"):
			pass # send email and things
		else:
			user.__setattr__(part, data['value'])
			user.save()
		return flask.jsonify({"status" : "JOY"})
		

	def showRegisterPage(self):
		return flask.render_template("pages/index/register.html")

	def showLoginPage(self):
		return flask.render_template("pages/index/login.html")

	def logout(self):
		if self.isUserLoggedIn():
			d = flask.session['user']
			del(self.LOGGED_USERS[d])
			del(flask.session['user'])
		return flask.redirect("/")
		
	def isUserLoggedIn(self):
		if "user" not in flask.session:
			return False
		id = flask.session['user']
		if id not in self.LOGGED_USERS:
			return False
		return True

	def getCurrentUser(self):
		if self.isUserLoggedIn():
			return self.LOGGED_USERS[flask.session['user']]["User"]
		return None

	def showHomePage(self):
		if not self.isUserLoggedIn():
			return flask.redirect(flask.url_for("LOGIN"))
		return flask.render_template("pages/user/landing.html", SessionToken = self.LOGGED_USERS[flask.session['user']]["SessionID"])

	def loginUser(self):
		data = flask.request.json
		if not self.LOGIN_VALIDATOR.validate(data):
			return  flask.jsonify({"status" : "NOJOY", "message" : self.LOGIN_VALIDATOR.ERROR})
		print("Data logged")
		user = User.get(User, {"uname" : data["uname"]})
		responce = JsonResponce()
		from app.framework.users import LoginUser
		if not LoginUser(user, data["password"]) or not user.active:
			responce.action("displayMessage" , "Email/Password invalid", "NOJOY")
		else:
			responce.action("displayMessage" , ("Welcome back %s" % (user.uname)))
			responce.action("redirect" , "/home")
			self.LOGGED_USERS[user.uid] = {"SessionID" : uuid.uuid4().hex, "User" : user}
			print("User Logged in")
		return responce.render()

	def registerUser(self):
		data = flask.request.json
		if not self.REGISTER_VALIDATOR.validate(data):
			return  flask.jsonify({"status" : "NOJOY", "message" : self.REGISTER_VALIDATOR.ERROR})
		print("Data logged")
		user = User()
		user.parse_dbo(data)
		resp = JsonResponce()
		from app.framework.users import RegisterUser
		if not RegisterUser(user, data['password']):
			resp.action("displayMessage", user.ERROR, "NOJOY")
		else:
			resp.action("displayMessage" , "An activation email has been sent!")
		return resp.render()

INSTANCE = UserPage()