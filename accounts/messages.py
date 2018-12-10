from api import APIMessage
from users.messages import RegisterMessage
import re

BIO_RE = re.compile(r"^$")

class SettingsMessage(RegisterMessage):

	REQUIRED = ["g-recaptcha-response"]
	

	def __init__(self, **kwargs):
		RegisterMessage.__init__(self, **kwargs)

	def test_biography(self, value:str):
		if not value:
			self.logError("biography","Your biography can not be empty")
		return bool(value)

	def test_gender(self, value:str):
		if value not in ["Male", "Female"]:
			self.logError("gender", "Please supply a valid gender")
			return False
		return True

	def test_interest(self, value:str):
		if value not in ["Men", "Women", "Both"]:
			self.logError("interest", "Please supply a valid sexual prefrence")
			return False
		return True

	def test_image(self, value:str):
		if not value.startswith("data:image/jpeg;base64,"):
			self.logError("image", "The image must be a jpeg")
			return False
		return True


class FieldUpdatedMessage(APIMessage):
	pass