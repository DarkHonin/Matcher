from users.messages import RegisterMessage
import re

BIO_RE = re.compile(r"^$")

class SettingsMessage(RegisterMessage):

	REQUIRED = ["g-recaptcha-response"]

	def test_biography(self, value:str):
		if not value:
			self.logError("biography","Your biography can not be empty")
		return bool(value)

	def test_image(self, value:str):
		if not value.startswith("data:image/jpeg;base64,"):
			self.logError("image", "The image must be a jpeg")
			return False
		return True
