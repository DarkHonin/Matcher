from app.database import DBDocument
from datetime import datetime
from bson import ObjectId

class Message(DBDocument):
	def __init__(self, author : ObjectId, message):
		DBDocument.__init__(self)
		self.author = author
		self.message = message
		self.time = datetime.now()
		self.read = False

class Chat(DBDocument):
	collection_name = "Chats"

	def __init__(self, author1 : ObjectId, author2 : ObjectId):
		DBDocument.__init__(self)
		self.date = datetime.now()
		self.authors = [
			{
				"user" : author1,
				"pending" : False
			},
			{
				"user" : author2,
				"pending" : False
			}
		]
		self.messages = []

	def get_other_user(self, current : ObjectId):
		for i in self.authors:
			if i["user"] != current:
				return i

	def accept(self, user : ObjectId):
		ok = True
		for i in self.authors:
			if i["user"] == user:
				i["pending"] = True
			if not i["pending"]:
				ok = False
		return ok

	def unread_count(self, uid : ObjectId):
		ret = 0
		for q in self.messages:
			if q.author != uid and not q.read:
				ret+=1
		return ret


	@property
	def user(self):
		from flask_jwt_extended import current_user
		for i in self.authors:
			if i["user"] != current_user._id:
				return i["user"]

	@staticmethod
	def get_for_ids(uid1 : ObjectId, uid2 : ObjectId):
		return Chat.get({"$and" : [{"authors" : {"$elemMatch" : {"user" : uid1}}}, {"authors" : {"$elemMatch" : {"user" : uid2}}}]})

	@staticmethod
	def get_unread(uid : ObjectId):
		ret = Chat.get({"messages" : {"$elemMatch" : {"author" : {"$ne":uid}, "read" : False}}})
		if ret and not isinstance(ret, list):
			ret = [ret]
		if not ret:
			ret = []
		return ret