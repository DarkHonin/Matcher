from database import DBDocument
import datetime
from flask import url_for
class Profile(DBDocument):

	collection_name = "Profiles"

	def __init__(self, user, fname, lname, dob):
		DBDocument.__init__(self)
		self.fname = fname
		self.lname = lname
		self.user = user._id
		self.biography = ""
		self.gender = "Unknown"
		self.interest = "Both"
		self.tags = []
		self.images = []
		self.location = [0, 0]
		self.dob = datetime.datetime.strptime(dob, "%Y-%m-%d")

	def set_tags(self, value:list):
		self.tags = value
		return value

	def set_fname(self, value):
		self.fname = value
		return value

	def set_lname(self, value):
		self.lname = value
		return value

	def set_gender(self, gender):
		self.gender = gender
		return gender

	def set_interest(self, interest):
		self.interest = interest
		return interest

	def set_biography(self, string):
		self.biography = string
		return string

	def set_images(self, image_64):
		import base64
		from app import APP
		import os
		from werkzeug.utils import secure_filename
		image_64 = str(image_64).replace("data:image/jpeg;base64,", "")
		bins = base64.b64decode(image_64)
		date = datetime.datetime.now()
		fn = "%s_%s_%s_%s_%s_%s.jpg" % (date.year, date.month, date.hour, date.minute, date.second, str(self._id))
		fd = open(os.path.join(APP.config['UPLOAD_FOLDER'], fn) , "wb+")
		fd.write(bins)
		fd.close()
		self.images.append(fn)
		return url_for("getUserImage", fn=fn)

	def age(self):
		return datetime.date.today().year - self.dob.year

	def complete(self):
		messages = []
		if self.gender not in ["Male", "Female"]:
			messages.append("Please select your biological gender")
		if len(self.biography) < 50:
			messages.append("Your biography must be atleast 50 characters long")
		if len(self.tags) < 5:
			messages.append("You need atleast 5 tags")
		if len(self.images) < 1:
			messages.append("You need atleast 1 profile image")
		return (not bool(messages), messages)