from database import DBDocument
from .user import User
import datetime

class UserInfo(DBDocument):
	def __init__(self, fname, lname):
		self.fname = fname
		self.lname = lname
		self.biography = ""
		self.gender = "Unset"
		self.interest = "Both"
		self._tags = []
		self.images = []
		self.location = [0, 0]
		self._dob = datetime.datetime.now()

	def activate(self):
		from systems.telemetry import Telemetry
		from flask import request
		import requests
		url = "http://api.ipstack.com/%s?access_key=c3d5cfa1b31c8989bb9c1d4f36cc096b" % request.environ['REMOTE_ADDR']
		response = requests.get(url).json()
		if not self.location:
			if(not response['latitude']):
				self.location = [0, 0]
			else:
				self.location = [response['latitude'], response["longitude"]]
			
		self.active = True
		self.save()

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
		if self.gender == "Unset":
			return False
		return True

	@property
	def tags(self):
		return self._tags

	@tags.setter
	def tags(self, string:str):
		import json
		self._tags = json.loads(string)

	@property
	def dob(self):
		try:
			return self._dob.date()
		except Exception:
			print("Invalid date set")

	@dob.setter
	def dob(self, st):
		if type(st) is not datetime.datetime:
			self._dob = datetime.datetime.strptime(st, "%Y-%m-%d")
			return
		self._dob = st

	@property
	def age(self):
		dt = datetime.date.today().year - self.dob.year
		return dt

	@property
	def fame(self):
		from systems.telemetry import Telemetry
		return Telemetry.forUser(self).fame()
		
	def toDisplaySet(self):
		dc = super().toDisplaySet()
		dc["age"] = self.age
		dc["fame"] = self.fame
		return dc