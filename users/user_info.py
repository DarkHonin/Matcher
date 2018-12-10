from database import DBDocument
import datetime
from flask import url_for
class UserInfo(DBDocument):

	collection_name = "UserDetails"

	def __init__(self, fname, lname, dob):
		DBDocument.__init__(self)
		self.fname = fname
		self.lname = lname
		self.biography = ""
		self.gender = "Unknown"
		self.interest = "Both"
		self.tags = []
		self.images = []
		self.location = [0, 0]
		self.dob = None

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

	@property
	def age(self):
		dt = datetime.date.today().year - self.dob.year
		return dt