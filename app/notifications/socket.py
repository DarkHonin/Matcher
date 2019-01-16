from flask_socketio import Namespace, emit, join_room
from flask_jwt_extended import decode_token
from flask import session
from . import Notification, UserNotifications
from bson import ObjectId
from app.chat import Chat

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
		chats = Chat.get_unread(current_user._id)
		Notifier.push_message_count(current_user._id, len(chats))
		Notifier.push_alert_count(current_user._id, len(UserNotifications.get_unread(current_user)))
		emit("online", {"id" : str(current_user._id)}, broadcast=True)
		print("%s::%s has come online" % (current_user._id, current_user.uname))

	def on_isOnline(self, id):
		from bson import ObjectId
		if ObjectId(id["id"]) in ONLINE:
			emit("online",  id)

	def on_disconnect(self):
		current_user = self.current_user
		ONLINE.remove(current_user._id)
		emit("offline", {"id" : str(current_user._id)}, broadcast=True)
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

	@staticmethod
	def push_message_count(uid : ObjectId, amount : int):
		from app import SOCKET
		SOCKET.emit("message_count", amount, room=str(uid), namespace="/notfications")

	@staticmethod
	def push_chat_count(uid : ObjectId, chat):
		from app import SOCKET
		SOCKET.emit("chat_count", {"count":chat.unread_count(uid), "chat_id":str(chat._id)}, room=str(uid), namespace="/notfications")
		

