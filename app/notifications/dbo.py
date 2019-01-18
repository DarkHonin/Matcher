from app.database import DBDocument
from app.users import User
from app.account import Telemetry
from datetime import datetime
from flask import url_for

class Notification(DBDocument):

	collection_name = "Notifications"

	ACTION_LIKE = "Like"
	ACTION_VIEW = "View"
	ACTION_MESSAGE = "Message"
	ACTION_LINKED = "Linked"

	def __init__(self, author : User, reciever : User, action : str):
		if action not in [self.ACTION_LIKE, self.ACTION_VIEW, self.ACTION_MESSAGE, self.ACTION_LINKED]:
			raise Exception("Invalid select action : "+action)
		self.author = author._id
		self.reciever = reciever._id
		self.action = action
		self.date = datetime.now()
		self.read = False

	@property
	def message(self):
		auth = User.get({"_id" : self.author}, {"uname" : 1})
		if self.action == self.ACTION_LIKE:
			return "%s liked your page" % auth["uname"]
		if self.action == self.ACTION_LINKED:
			return "%s and your account is now linked, you can chat" % auth["uname"]
		if self.action == self.ACTION_VIEW:
			return "%s looked at your profile" % auth["uname"]
		if self.action == self.ACTION_MESSAGE:
			return "%s left you a message" % auth["uname"]

	@property
	def author_url(self):
		return url_for("accounts.public_profile", uid=self.author)

	@property
	def age(self):
		return (datetime.now() - self.date)

class UserNotifications:

	@staticmethod
	def notify(notif : Notification):
		tel = Telemetry.get({"user" : notif.reciever})
		if notif.author in tel.blocked:
			return
		
		print("Sending notification")
		from .socket import Notifier
		Notifier.push_notification(notif)
		Notifier.push_alert_count(notif.reciever, len(UserNotifications.get_unread(User(_id=notif.reciever))))
		notif.save()

	@staticmethod
	def get_read(current_user):
		unread = Notification.get({"reciever" : current_user._id, "read" : True, "action" : {"$ne" : Notification.ACTION_MESSAGE}})
		if not unread:
			return []
		if not isinstance(unread, list):
			unread = [unread]
		unread.sort(key=lambda x: x.date, reverse=True)
		return unread

	@staticmethod
	def get_unread(current_user : User):
		unread = Notification.get({"reciever" : current_user._id, "read" : False, "action" : {"$ne" : Notification.ACTION_MESSAGE}})
		if not unread:
			return []
		if not isinstance(unread, list):
			unread = [unread]
		unread.sort(key=lambda x: x.date, reverse=True)
		return unread
	
	@staticmethod
	def get_messages(current_user):
		unread = Notification.get({"reciever" : current_user._id, "read" : False, "action" : Notification.ACTION_MESSAGE})
		if not unread:
			return []
		if not isinstance(unread, list):
			unread = [unread]
		return unread