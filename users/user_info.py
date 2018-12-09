from database import DBDocument
import datetime

class UserInfo(DBDocument):

	collection_name = "UserDetails"

	def __init__(self, fname, lname, dob):
		self.fname = fname
		self.lname = lname
		self.biography = ""
		self.gender = "Unset"
		self.interest = "Both"
		self._tags = []
		self.images = []
		self.location = [0, 0]
		self.dob = None

	@property
	def tags(self):
		return self._tags

	@tags.setter
	def tags(self, string:str):
		import json
		self._tags = json.loads(string)

	def set_biography(self, string):
		self.__dict__["biography"] = string

	@property
	def age(self):
		dt = datetime.date.today().year - self.dob.year
		return dt