from systems.database import DBDocument
from systems.users.user import User
from datetime import datetime

CHAT_PENDING = 0
CHAT_ACCEPTED = 1
CHAT_DENIED = -1
CHAT_BLOCKED = -2

class UserSession(DBDocument):
	def __init__(self):
		DBDocument.__init__(self)
		self.hasPending = False
		self.chatState = CHAT_PENDING

class ChatMessage(DBDocument):
	def __init__(self, author : User, message : str):
		self.author = author._id
		self.message = message
		self.sentOn = datetime.now()

class Chat(DBDocument):
	collection_name =  "Chat"

	def __init__(self, user1 : User, user2 : User):
		DBDocument.__init__(self)
		self.users = {user1._id : UserSession(), user2._id : UserSession()}
		self.messages = []

	def sendMessage(self, user : User, message : str):
		if user._id not in self.users:
			return False
		self.messages.append(ChatMessage(user, message))
		self.save()
		return True

	def user(self, notID):
		hold = self.ids
		hold.remove(notID)
		user = User.get({"_id" : hold.pop()}, {"uname" : 1, "info.images" : 1, "info.class" : 1, "last_online" : 1, "class" : 1})
		return user

	@staticmethod
	def spawnChat(user1, user2):
		if user1._id in user2.telemetry._blocked or user2._id in user1.telemetry._blocked:
			return False
		user2.telemetry.postMessage("%s has linked with you, go to messages to start chatting" % user1.uname, user1._id)
		user1.telemetry.postMessage("%s has linked with you, go to messages to start chatting" % user2.uname, user2._id)
		user1.save()
		user2.save()
		if not Chat.get({"ids" : {"$all" : [user1._id, user2._id]}}):
			Chat(user1, user2).save()