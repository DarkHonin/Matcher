from app.database import DBDocument, Editor
from datetime import datetime
from app.users import User

class Account(DBDocument):

	collection_name = "Accounts"

	GENDER_MALE = "Male"
	GENDER_FEMALE = "Female"
	GENDER_UNSET = "Unknown"

	def __init__(self, user : User, **kwargs):
		DBDocument.__init__(self)
		self.user = user._id
		self.fname = kwargs["fname"]
		self.lname = kwargs["lname"]
		self.gender = self.GENDER_UNSET
		self.dob = datetime.strptime(kwargs["dob"], "%Y-%m-%d")
		self.tags = []
		self.images = []

class AccountEditor(Editor):
	
	"""
		prep image:
		
		gets the base 64 of the image
		saves it locally
		returns uuid of the image file
	"""

	def prep_image(self, image_data):
		pass
