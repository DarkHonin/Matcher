from app.database import DBDocument
from datetime import datetime
from bson import ObjectId

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

	def accept(self, user : ObjectId):
		for i in self.authors:
			if i["user"] == user:
				i["pending"] = True

	@property
	def user(self):
		from flask_jwt_extended import current_user
		for i in self.authors:
			if i["user"] != current_user._id:
				return i["user"]

	@staticmethod
	def get_for_ids(uid1 : ObjectId, uid2 : ObjectId):
		return Chat.get({"$and" : [{"authors" : {"$elemMatch" : {"user" : uid1}}}, {"authors" : {"$elemMatch" : {"user" : uid2}}}]})