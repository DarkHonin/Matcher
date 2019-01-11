from app.api import APIValidatingMessage, APIException, APISuccessMessage
import re
from datetime import datetime

EMAIL_RE = re.compile(r"^[a-zA-Z0-9_\.\-]+@[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+$")
UNAME_RE = re.compile(r"^[a-zA-Z0-9]{5,10}$")
PASSW_RE = re.compile(r"^(?=.*[A-Z])(?=.*\d)(?=.*[a-z]).{6,20}$")
PNAME_RE = re.compile(r"^[A-Z][a-z]+$")

class RecoverMessage(APIValidatingMessage):
	REQUIRED = ["email", "g-recaptcha-response"]
	ONLY_ACCEPTS = ["email", "g-recaptcha-response"]

	def test_email(self, value:str):
		if not EMAIL_RE.match(value):
			self.logError("email", "Your email is invalid")
			return False
		return True

class LoginMessage(APIValidatingMessage):

	REQUIRED = ["uname", "password", "g-recaptcha-response"]
	ONLY_ACCEPTS = ["uname", "password", "g-recaptcha-response"]

	def test_uname(self, value:str):
		if not UNAME_RE.match(value):
			self.logError("uname", "The username can only be alphanumerical and between 5 and 10 characters")
			return False
		return True

	def test_password(self, value:str):
		if not PASSW_RE.match(value):
			self.logError("password",  "A password must contain atleast one uppercase, lowecase and numeric character")
			return False
		return True

	def test_g_recaptcha_response(self, value:str):
		from app import APP
		if APP.config.get("CAPTCHA_DISABLE"):
			self.logError("captcha", "The captcha has been disabled for testing")
			return True
		import requests
		import json
		secret = APP.config.get("CAPTCHA_SECRET")
		payload = {'response':value, 'secret':secret}
		try:
			response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
		except requests.exceptions.ConnectionError:
			self.logError("captcha", "Could link up with captcha server, please try again")
			return False
		response_text = json.loads(response.text)
		if not response_text['success']:
			self.logError("captcha", "The captcha was invalid")
			return False
		return True

class RegisterMessage(LoginMessage):

	REQUIRED = ["email", "dob", "fname", "lname"] + LoginMessage.REQUIRED
	ONLY_ACCEPTS = ["email", "dob", "fname", "lname"] + LoginMessage.ONLY_ACCEPTS

	def test_email(self, value:str):
		if not EMAIL_RE.match(value):
			self.logError("email", "Your email is invalid")
			return False
		return True

	def test_dob(self, value:str):
		try:
			delta = datetime.now().year - datetime.strptime(value, "%Y-%m-%d").year
			if delta < 18:
				self.logError("dob", "You must be 18 or older to use this APP")
				return False
		except Exception as e:
			self.logError("dob", "The date was improperly formatted")
			return False
		return True

	def test_fname(self, value:str):
		if not PNAME_RE.match(value):
			self.logError("fname", "A name must start with one capital letter and is only alphabetical")
			return False
		return True

	def test_lname(self, value:str):
		if not PNAME_RE.match(value):
			self.logError("lname", "A name must start with one capital letter and is only alphabetical")
			return False
		return True

class APIDuplicateUser(APIException):
	pass

class APIInvalidUser(APIException):
	def __init__(self):
		APIException.__init__(self, message="Invalid Username / Password")

class APIUserNotActive(APIException):
	def __init__(self):
		APIException.__init__(self, message="Please activate your account before loggin in")
