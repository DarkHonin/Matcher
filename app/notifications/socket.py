from flask_socketio import Namespace, emit, join_room
from flask_jwt_extended import decode_token
from flask import session
from . import Notification, UserNotifications

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

class Notifier(Namespace):

	ONLINE = []

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
		self.ONLINE.append(current_user._id)
		join_room(str(current_user._id))
		emit("online", {"id" : str(current_user._id)}, broadcast=True)
		emit("notif_count", {"messages" : len(UserNotifications.get_messages(current_user)), "alerts" : len(UserNotifications.get_unread(current_user))})
		print("%s::%s has come online" % (current_user._id, current_user.uname))

	def on_disconnect(self):
		current_user = self.current_user
		self.ONLINE.remove(current_user._id)
		emit("offline", {"id" : str(current_user._id)}, broadcast=True)
		print("%s::%s has gone offline" % (current_user._id, current_user.uname))
	
	def on_isOnline(self, id):
		from bson import ObjectId
		if ObjectId(id["id"]) in self.ONLINE:
			emit("online",  id)

	def on_get_notif_count(self):
		current_user = self.current_user
		emit("notif_count", {"messages" : len(UserNotifications.get_messages(current_user)), "alerts" : len(UserNotifications.get_unread(current_user))})

	@staticmethod
	def push_notification(notification : Notification):
		if notification.reciever not in Notifier.ONLINE:
			return
		from app import SOCKET
		SOCKET.emit("notification", notification.message, room=str(notification.reciever), namespace="/notfications")
		

