import re

class Field:
	def __init__(self, key : str, stack, required=False, label = None, Type="text", args=()):
		self.required = required
		self.stack = stack
		self.fault = None
		self.args = args
		self.key = key
		self.type = Type
		if not label:
			self.label = key
		else:
			self.label = label

	def validate(self, param):
		for m, f in self.stack.items():
			if self.args:
				res = f(param, self.args)
			else:
				res = f(param)
			if(not res):
				self.fault = m
				return False
		return True

	def getHTMLValue(self, value):
		return value

	def template(self):
		if self.type in ["text", "password", "email"]:
			return "fields/text_style.html"
		if self.type is "enum":
			return "fields/enum_style.html"
		if self.type is "blob":
			return "fields/blob_style.html"

class Validator:

	ONLY_CHARS = re.compile(r"^[a-zA-Z]+\Z")
	ONLY_ALPHANUMERIC = re.compile(r"^[a-zA-Z0-9]+\Z")
	STARTS_UPPERCASE = re.compile(r"^[A-Z]")
	HAS_SPACES = re.compile(r"\s+")
	IS_EMAIL   = re.compile(r"^[a-zA-Z0-9_\.\-]+@[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+$")

	VALID = "JOY"
	INVALID = "NOJOY"

	def __init__(self, fields):
		self.fields = fields
		self.ERROR = None

	def validate(self, data : dict, ignoreRequired = False):
		for field in self.fields:
			if field.key in data:
				if not field.validate(data[field.key]):
					self.ERROR = field.fault
					return False
			elif field.required and not ignoreRequired:
				self.ERROR = ("'%s' is a required field" % field.label)
				return False
		return True

	def fieldFor(self, key):
		for f in self.fields:
			if key == f.key:
				return f
		return None

	@staticmethod
	def noSpaces(test):
		return not Validator.HAS_SPACES.match(test)

	@staticmethod
	def isLonger(test, length):
		return len( test) > length

	@staticmethod
	def oneOf(test, arr):
		return test in arr

	@staticmethod
	def enum(test, arr):
		return 0 <= int(test) < len(arr)

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
		if app.config.get("CAPTCHA_DISABLE"):
			return True
		import requests
		import json
		secret = app.config.get("CAPTCHA_SECRET")
		payload = {'response':test, 'secret':secret}
		response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
		response_text = json.loads(response.text)
		return response_text['success']
