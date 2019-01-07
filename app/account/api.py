from app.users.api import RegisterMessage
from werkzeug.security import generate_password_hash
from app.database import DBDocument


class OptionSet(RegisterMessage):
	
	REQUIRED = ["g-recaptcha-response"]
	ONLY_ACCEPTS = RegisterMessage.ONLY_ACCEPTS + ["image", "tags", "gender"]

	FIELDS = ["uname", "password", "lname", "fname", "gender", "image", "tags", ]

	@property
	def setting(self):
		for k in self.FIELDS:
			if hasattr(self, k):
				return (k , getattr(self, k))

	def test_gender(self, value):
		from app.account import Account
		options = [Account.GENDER_FEMALE, Account.GENDER_MALE]
		if value not in options:
			self.logError("gender", "Your biological gender must be iether '%s' of '%s'" % (Account.GENDER_MALE, Account.GENDER_FEMALE))
			return False
		return True
