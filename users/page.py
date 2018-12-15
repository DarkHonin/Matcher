from database import DBDocument
import datetime
from flask import url_for, session
from .user import User

class Page(DBDocument):

	collection_name = "PageInfo"

	def __init__(self):
		DBDocument.__init__(self)
		self.liked_by = []
		self.viewed_by = []
		self.blacklist = []
		self.alerts = []

	@property
	def isLiked(self):
		return session["user"]._id in self.liked_by

	def fame(self):
		if not self.viewed_by:
			return 0
		return (len(self.liked_by)/len(self.viewed_by))*1000

	def view(self, viewer : User):
		if (viewer._id not in self.viewed_by):
			self.viewed_by.append(viewer._id)
			return True
		return False

	def like(self, liker:User):
		if liker._id not in self.liked_by:
			self.liked_by.append(liker._id)
			return True
		else:
			self.liked_by.remove(liker._id)
		return False

	def block(self, blocked:User):
		if blocked._id not in self.blacklist:
			self.blacklist.append(blocked._id)
		else:
			self.blacklist.remove(blocked._id)
		return blocked._id not in self.blacklist

	def getUnread(self):
		ret = []
		for i in self.alerts:
			if not i.seen:
				ret.append(i.message)
		return ret