from app.api import APIException

class APIInvalidEmail(APIException):
	def __init__(self):
		APIException.__init__(self, message="The provided email is invalid")

class APICouldNotConnectToMailServer(APIException):
	def __init__(self):
		APIException.__init__(self, message="The email service is currently unavailable, please try again later")

class APIInvalidToken(APIException):
	def __init__(self):
		APIException.__init__(self, message="Invalid / Missing token, please try again")