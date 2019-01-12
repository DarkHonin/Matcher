from app.database import DBDocument
from .api import APIDuplicateUser, APIInvalidUser
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_jwt_extended import set_access_cookies, set_refresh_cookies, create_access_token, create_refresh_token
import string
import random
class User(DBDocument):

	@staticmethod
	def activate_account(resource):
		resource.active = True
		resource.verified = True
		resource.save()
		return {"displayMessage" : {"message" : "Your account has now been activated"}, "redirect":"accounts.profile"}

	@staticmethod
	def verify_email(resource):
		resource.verified = True
		resource.save()
		return {"displayMessage" : {"message" : "Your email has been verified"}, "redirect":"accounts.profile"}

	@staticmethod
	def recover_account(resource):
		from app import EMAIL_CLIENT
		from flask_mail import Message
		pwd = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(15))
		npw = generate_password_hash(pwd)
		resource.password = npw
		resource.save()
		msg = Message("Pasword has been reset",recipients=[resource.email], body="Username : %s\nPassword : %s\n" % (resource.uname, pwd))
		EMAIL_CLIENT.send(msg)
		return {"displayMessage" : {"message" : "Your password has been rest, user the hash in the email to log in"}}

	collection_name = "Users"

	def  __init__(self, **kwargs):
		DBDocument.__init__(self)
		self.uname = kwargs["uname"]
		self.email = kwargs["email"]
		self.password = generate_password_hash(kwargs["password"])
		self.active = False
		self.login_location = None
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
		access_token = create_access_token(identity=self)
		refresh_token = create_refresh_token(identity=self)
		set_refresh_cookies(responce, refresh_token)
		set_access_cookies(responce, access_token)
		self.resolve_location()
		self.save()
		return access_token

	def resolve_location(self):
		print("geting location")
		from flask import request
		import requests
		ip = request.environ['REMOTE_ADDR']
		if ip == "127.0.0.1":
			ip = requests.get("http://api.ipify.org").text
		url = "http://api.ipstack.com/%s?access_key=c3d5cfa1b31c8989bb9c1d4f36cc096b" % ip
		response = requests.get(url).json()
		self.location = {"region_name" : (response["region_name"] + " " + response["country_name"]), "city" : response["city"]}
		print("Location discovered:",self.location)

	@property
	def isOnline(self):
		return False
