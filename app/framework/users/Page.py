from app.framework import Page
from app.framework.users import User
from app.framework import Token, Page, JsonResponce
from app.framework.validator import *
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


	def __init__(self):
		 Page.__init__(self, {
            "/:INDEX:GET" : self.showLoginPage,
            "/login:LOGIN:GET" : self.showLoginPage,
            "/login:LOGIN_ACTION:POST" : self.loginUser,
            "/register:REGISTER:GET" : self.showRegisterPage,
            "/register:REGISTER_ACTION:POST" : self.registerUser,
        })

	def showRegisterPage(self):
		return flask.render_template("pages/index/register.html")

	def showLoginPage(self):
		return flask.render_template("pages/index/login.html")

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
