from database import DBDocument
import datetime
from flask import url_for
from .user import User

class message(DBDocument):
	def __init__(self, message):
		DBDocument.__init__(self)
		self.created = datetime.datetime.now()
		self.message = message
		self.seen = False

class Page(DBDocument):

	collection_name = "PageInfo"

	def __init__(self):
		DBDocument.__init__(self)
		self.last_event = datetime.datetime.now()
		self.created_on = datetime.datetime.now()
		self.liked_by = []
		self.viewed_by = []
		self.blacklist = []
		self.alerts = []
		self.last_message_index = 0

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
			self.alerts.append(message("%s just viewed your page" % viewer.uname))

	def like(self, liker:User):
		if liker._id not in self.liked_by:
			self.liked_by.append(liker._id)
			self.last_event = datetime.datetime.now()
		else:
			self.liked_by.remove(liker._id)
		if liker._id not in self.blacklist:
			self.alerts.append(message("%s just %s your page" % (liker.uname, "liked" if liker._id in self.liked_by else "unliked")))
		return liker._id not in self.liked_by

	def getUnread(self):
		ret = []
		for i in self.alerts:
			if not i.seen:
				ret.append(i.message)
		return ret