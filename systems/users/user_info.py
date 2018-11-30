from systems.database import DBDocument
from systems.users.user import User
from systems.properties import FIRSTNAME, LASTNAME, GENDER, INTEREST, TAGS, BIOGRAPHY

class UserInfo(User):
	def __init__(self, fname, lname, **kwargs):
		User.__init__(self, **kwargs)
		self.fname = fname
		self.lname = lname
		self.biography = ""
		self.gender = ""
		self.interest = ""
		self._tags = []
		self.images = []
		self.location = [0, 0]

	def activate(self):
		from systems.telemetry import Telemetry
		from flask import request
		import requests
		url = "http://api.ipstack.com/%s?access_key=c3d5cfa1b31c8989bb9c1d4f36cc096b" % request.environ['REMOTE_ADDR']
		response = requests.get(url).json()
		self.location = [response['latitude'], response["longitude"]]
		if not self.location[0]:
			self.location = [0, 0]
		Telemetry(self, 
			["Male", "Prefer not to say", "Female"].index(self.gender) - 1,
			["Men", "Both", "Women"].index(self.interest) - 1
		).save()
		self.active = True
		self.save()

	@property
	def fields(self):
		return [BIOGRAPHY, FIRSTNAME, LASTNAME, GENDER, INTEREST, TAGS]

	@property
	def imageCount(self):
		return len(self.images)

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

	def getFields(self):
		return super().getFields() + ["user", "fname", "lname", "biography", "gender", "interest", "_tags", "images", "location"]