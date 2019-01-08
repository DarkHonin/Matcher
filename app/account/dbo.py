from app.database import DBDocument, Editor
from datetime import datetime
from app.users import User

class Account(DBDocument):

	collection_name = "Accounts"

	GENDER_MALE = "Male"
	GENDER_FEMALE = "Female"
	GENDER_UNSET = "Unknown"

	INTEREST_UNSET = "Unknown"
	INTEREST_MEN = "Men"
	INTEREST_WOMEN = "Women"
	INTEREST_BOTH = "Men & Women"

	def __init__(self, user : User, **kwargs):
		DBDocument.__init__(self)
		self.user = user._id
		self.fname = kwargs["fname"]
		self.lname = kwargs["lname"]
		self.gender = self.GENDER_UNSET
		self.interest = self.INTEREST_UNSET
		self.dob = datetime.strptime(kwargs["dob"], "%Y-%m-%d")
		self.tags = []
		self.images = []
		self.biography = ""

	@property
	def complete(self):
		if len(self.biography) < 25 or self.gender == self.GENDER_UNSET or self.interest == self.INTEREST_UNSET or len(self.tags) < 5 or not self.images:
			return False
		return True

	@property
	def problems(self):
		ret = []
		if self.gender == self.GENDER_UNSET:
			ret.append("Please select your gender")
		if self.interest == self.INTEREST_UNSET:
			ret.append("Please select your 'interest'")
		if len(self.tags) < 5:
			ret.append("Please select atelast 5 tags")
		if not self.images:
			ret.append("Your profile needs atleast 1 image")
		if len(self.biography) < 25:
			ret.append("Your biography must contain atleast 25 characters")
		return ret