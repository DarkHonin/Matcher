from systems.database import DBDocument
from systems.users.user import User
from systems.properties import FIRSTNAME, LASTNAME, GENDER, INTEREST, TAGS, BIOGRAPHY

class UserInfo(DBDocument):
	def __init__(self,user:User, fname, lname, biography, gender, interest, tags, images, location):
		DBDocument.__init__(self)
		self._user = user
		self.fname = fname
		self.lname = lname
		self.biography = biography
		self.gender = gender
		self.interest = interest
		self._tags = tags
		self.images = images
		self.location = location

	@property
	def fields(self):
		return [BIOGRAPHY, FIRSTNAME, LASTNAME, GENDER, INTEREST, TAGS]

	@property
	def imageCount(self):
		return len(self.images)

	@property
	def user(self):
		return str(self._user._id)

	@property
	def complete(self):
		if not self.biography:
			return False
		if len(self.tags) < 5:
			return False
		if len(self.images) < 1:
			return False
		return True

	@property
	def tags(self):
		return self._tags

	@tags.setter
	def tags(self, string:str):
		import json
		self._tags = json.loads(string)

	@user.setter
	def user(self, id:str):
		self._user = User.get({"_id" : id}, {"hash" : 0})

	def getFields(self):
		return ["user", "fname", "lname", "biography", "gender", "interest", "_tags", "images", "location"]

	def getCollectionName(self):
		return "UserInfo"