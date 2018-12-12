from database import DBDocument
import datetime
from flask import url_for
from .user import User
class Page(DBDocument):

	collection_name = "PageInfo"

	def __init__(self):
		DBDocument.__init__(self)
		self.last_event = datetime.datetime.now()
		self.created_on = datetime.datetime.now()
		self.liked_by = []
		self.viewed_by = []
		self.blacklist = []

	def fame(self):
		base = datetime.datetime.now() - self.created_on
		sinceLastEdit = datetime.datetime.now() - self.last_event
		delta = base - sinceLastEdit
		print("time since last edit: %s" % delta)
		prs = delta / base
		print(prs, "-----------------")

	def view(self, viewer : User):
		if (viewer._id not in self.blacklist and viewer._id not in self.viewed_by):
			self.viewed_by.append(viewer._id)
			self.last_event = datetime.datetime.now()