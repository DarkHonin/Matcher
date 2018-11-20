import re

class Validator:

	ONLY_CHARS = re.compile(r"^[a-zA-Z]+\Z")
	ONLY_ALPHANUMERIC = re.compile(r"^[a-zA-Z0-9]+\Z")
	STARTS_UPPERCASE = re.compile(r"^[A-Z]")
	HAS_SPACES = re.compile(r"\s+")

	VALID = "JOY"
	INVALID = "NOJOY"

	def __init__(self, stages):
		self.stages = stages

	def validate(self, data : dict):
		for i in data:
			if i in self.stages:
				for s in self.stages[i]:
					if type(s) is list:
						if(not s[0](data[i], *s[1])):
							return {"state" : "NOJOY", "DIED" : s[0].__name__}
					else:
						if(not s(data[i])):
							return {"state" : "NOJOY", "DIED" : s.__name__}
		return {"state" : "JOY"}

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
	def isValidName(test):
		return Validator.ONLY_CHARS.match(test) and Validator.STARTS_UPPERCASE.match(test)
