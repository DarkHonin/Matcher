import re

class Validator:

	ONLY_CHARS = re.compile(r"^[a-zA-Z]+\Z")
	ONLY_ALPHANUMERIC = re.compile(r"^[a-zA-Z0-9]+\Z")
	STARTS_UPPERCASE = re.compile(r"^[A-Z]")
	HAS_SPACES = re.compile(r"\s+")
	IS_EMAIL   = re.compile(r"^[a-zA-Z0-9_\-]+@[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+$")

	VALID = "JOY"
	INVALID = "NOJOY"

	def __init__(self, stages):
		self.fields = stages
		self.STATUS = {"status" : "JOY"}

	def validate(self, data : dict):
		for field in data:
			if field in self.fields:
				_field = self.fields[field]
				for k, stage in _field.items():
					if type(stage) is list:
						if(not stage[0](data[field], *stage[1])):
							self.STATUS = {"status" : "NOJOY", "action":"field_error", "message" : k}
							return False
					else:
						if(not stage(data[field])):
							self.STATUS = {"status" : "NOJOY", "action":"field_error", "message" : k}
							return False
		return True

	@staticmethod
	def noSpaces(test):
		return not Validator.HAS_SPACES.match(test)

	@staticmethod
	def isLonger(test, length):
		return len( test) > length

	@staticmethod
	def hasSpaces(test):
		return Validator.HAS_SPACES.match(test)

	@staticmethod
	def isAlphaNumeric(test):
		return Validator.ONLY_ALPHANUMERIC.match(test)

	@staticmethod
	def isEmail(test):
		return Validator.IS_EMAIL.match(test)

	@staticmethod
	def isValidName(test):
		return Validator.ONLY_CHARS.match(test) and Validator.STARTS_UPPERCASE.match(test)

	@staticmethod
	def checkCaptcha(test):
		from app import app
		import requests
		import json
		secret = app.config.get("CAPTCHA_SECRET")
		payload = {'response':test, 'secret':secret}
		response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
		response_text = json.loads(response.text)
		return response_text['success']
