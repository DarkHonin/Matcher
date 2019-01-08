from app.database import DBDocument
from .api import APIDuplicateUser, APIInvalidUser
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_jwt_extended import set_access_cookies, set_refresh_cookies, create_access_token, create_refresh_token

class User(DBDocument):

	@staticmethod
	def activate_account(resource):
		resource.active = True
		resource.verified = True
		resource.save()
		return "Your account has now been activated"

	@staticmethod
	def verify_email(resource):
		resource.verified = True
		resource.save()
		return "Your email has been verified"

	collection_name = "Users"

	def  __init__(self, **kwargs):
		DBDocument.__init__(self)
		self.uname = kwargs["uname"]
		self.email = kwargs["email"]
		self.password = generate_password_hash(kwargs["password"])
		self.active = False
		self.verified = False

	@staticmethod
	def defineKeys(col):
		col.create_index(("uname"), unique=True)
		col.create_index(("email"), unique=True)

	def DuplicateKeyError(self):
		raise APIDuplicateUser(message="Username / Email already in use")

	def login(self, password, responce):
		if not check_password_hash(self.password, password):
			raise APIInvalidUser()
		access_token = create_access_token(identity={"uname" : self.uname, "id" : str(self._id)})
		refresh_token = create_refresh_token(identity={"uname" : self.uname, "id" : str(self._id)})
		set_access_cookies(responce, access_token)
		set_refresh_cookies(responce, refresh_token)
