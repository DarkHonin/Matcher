from app.database import DBDocument, Callback
from uuid import uuid4


class Token(DBDocument):

	collection_name = "Tokens"

	def __init__(self, callback : Callback, resource, tp="Auth"):
		DBDocument.__init__(self)
		from app import APP
		if APP.config.get("CAPTCHA_DISABLE"):
			self.token = APP.config.get("TESTING_TOKEN")
		else:
			self.token = str(uuid4())
		self.callback = callback
		self.resource = resource
		self.type = tp

	@staticmethod
	def defineKeys(col):
		col.create_index(("resource"), unique=True)

	def redeem(self):
		return self.callback.resolve()