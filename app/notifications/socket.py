from flask_socketio import Namespace, emit, join_room, leave_room
from flask_jwt_extended import decode_token
from flask import session
from . import Notification, UserNotifications
from bson import ObjectId
from app.chat import Chat, Message
from datetime import datetime

"""
	TO-DO:
		Like notifications
		View notifications
		Linked notifications
		Ignore blocked accounts

		Messaging:
			View
			Pending 'Like backs'
			Linked accounts
			Exclude blocked accounts
"""
ONLINE = []

class Notifier(Namespace):


	def __init__(self):
		Namespace.__init__(self, namespace="/notfications")
	
	#Get current user
	@property
	def current_user(self):
		from app.users import User
		from bson import ObjectId
		if "token" not in session:
			raise Exception(message="Need token")
		token = decode_token(session["token"])
		return User.get({"_id" : ObjectId(token["identity"]['id'])}, {"hash" : 0})

	def on_connect(self):
		current_user = self.current_user
		ONLINE.append(current_user._id)
		join_room(str(current_user._id))
		self.push_chat_count(current_user._id)
		self.push_alert_count(current_user._id, len(UserNotifications.get_unread(current_user)))
		emit("online", {"id" : str(current_user._id)}, broadcast=True)
		print("%s::%s has come online" % (current_user._id, current_user.uname))

	def on_isOnline(self, id):
		from bson import ObjectId
		if ObjectId(id["id"]) in ONLINE:
			emit("online",  id)

	def on_disconnect(self):
		current_user = self.current_user
		ONLINE.remove(current_user._id)
		if "current_chat" in session:
			leave_room(session["current_chat"])
		leave_room(str(current_user._id))
		emit("offline", {"id" : str(current_user._id), "time" : datetime.now()}, broadcast=True)
		print("%s::%s has gone offline" % (current_user._id, current_user.uname))

	def on_get_notif_count(self):
		current_user = self.current_user
		emit("notif_count", {"messages" : len(UserNotifications.get_messages(current_user)), "alerts" : len(UserNotifications.get_unread(current_user))})

	@staticmethod
	def push_notification(notification : Notification):
		if notification.reciever not in ONLINE:
			return
		from app import SOCKET
		SOCKET.emit("notification", notification.message, room=str(notification.reciever), namespace="/notfications")

	@staticmethod
	def push_alert_count(uid : ObjectId, amount : int):
		from app import SOCKET
		SOCKET.emit("alert_count", amount, room=str(uid), namespace="/notfications")


	# Updates the count of unread messages in a chat
	@staticmethod
	def push_message_count(uid : ObjectId, chat : Chat):
		from app import SOCKET
		SOCKET.emit("message_count", {"count":chat.unread_count(uid), "chat_id":str(chat._id)}, room=str(uid), namespace="/notfications")

	# Updates the amount of chats with unread messages
	@staticmethod
	def push_chat_count(uid : ObjectId): #uid of the user to push to
		from app import SOCKET
		print("Pushing chat count to ", uid)
		chats = Chat.get_unread(uid)
		print("Unread", len(chats))
		SOCKET.emit("chat_count", len(chats), room=str(uid), namespace="/notfications")

	def prepare_messages(self, messages):
		ret = []
		for i in messages:
			ret.append(
				{"user" : str(i.author),
				"message" : i.message,
				"time" : str(i.time)
				}
			)
		return ret

	# Chat select, switcher room and returns message history
	def on_get_messages(self, id):
		chat = Chat.get({"_id":ObjectId(id["id"])})
		for i in chat.authors:
			if not i["pending"]:
				return emit("chat_pending", {"chat_id" : id["id"]})
		if "current_chat" in session:
			leave_room(session["current_chat"])
		join_room(str(chat._id))
		session["current_chat"] = str(chat._id)
		emit("show_chat", {"messages" : self.prepare_messages(chat.messages), "chat_id" : id["id"]})
		current_user = self.current_user
		self.push_chat_count(current_user._id)

	# a message has been sent ffrom a client
	def on_message_send(self, message, chat_id):
		print("message sent")
		if not message:
			return 
		current_user = self.current_user
		#Spawn message object/ add/ save
		ms = Message(current_user._id, message)
		chat = Chat.get({"_id":ObjectId(chat_id)})
		chat.messages.append(ms)
		chat.save()
		emit("message_get", {"message" : {"user" : str(current_user._id),
				"message" : ms.message,
				"time" : str(ms.time)
				}}, broadcast=True)
		self.push_chat_count(chat.get_other_user(current_user._id))

	def on_read(self, chat_id):
		print("chat read")
		chat = Chat.get({"_id" : ObjectId(chat_id)})
		current_user = self.current_user
		for q in chat.messages:
			if q.author != current_user._id and not q.read:
				q.read = True
		chat.save()
		self.push_message_count(current_user._id, chat)
		self.push_chat_count(current_user._id)
		
		

