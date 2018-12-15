from flask_socketio import Namespace, emit, join_room, leave_room
from flask import session
from users import User
from users.user_info import UserInfo
from users.page import Page
from database import DBDocument
import datetime
from api import APISuccessMessage, APIException, APIMessage

class APIButtonChange(APIMessage):
	pass

class message(DBDocument):
	def __init__(self, message):
		DBDocument.__init__(self)
		self.created = datetime.datetime.now()
		self.message = message
		self.seen = False

class MessageSockets(Namespace):

	INSTANCE = None

	def __init__(self):
		Namespace.__init__(self, "/messages")
		self.rooms = {}
		MessageSockets.INSTANCE = self

	def on_connect(self):
		if session["user"].uname not in self.rooms:
			self.rooms[session["user"].uname] = Page.get({"_id" : session["user"].page})
		print("user has come online :", session["user"].uname)
		join_room(session["user"].uname)
		emit("now_online", {"user" : session["user"].uname}, broadcast=True)
		self.checkProfileStatus()

	def on_disconnect(self):
		if session["user"] not in self.rooms:
			return
		leave_room(session["user"].uname)
		print("user now offline :", self.rooms[session["user"]].user.uname)
		emit("now_offline", {"user" : self.rooms[session["user"]].user.uname}, broadcast=True)

	def sendMessage(self, user : User, message : str):
		from app import APP, SOCKETS
		with APP.app_context():
			if user.uname in self.rooms:
				print("Emmiting to room ", user.uname)
				SOCKETS.emit("accountStatus", APISuccessMessage(message=message).toDict(), room=user.uname, namespace="/messages")

	def on_like(self, data):
		suname = data["subject"]
		if suname not in self.rooms:
			usr = User.get({"uname" : suname}, {"page" : 1, "class" : 1})
			self.rooms[suname] = Page.get({"_id" : usr.page})
		else:
			self.rooms[suname].sync()
		lk = self.rooms[suname].like(session["user"])
		emit("general", APIButtonChange(id="like", innerHTML=("Like" if not lk else "Unlike")).toDict())
		self.rooms[suname].save()
		print("Liking?", suname)
		if suname in self.rooms:
			if session["user"]._id not in self.rooms[suname].blacklist:
				emit("accountStatus", APISuccessMessage(message="%s has %s your page" % (session["user"].uname, "liked" if lk else "unliked"), state=lk).toDict(), room=suname)

	def on_block(self, data):
		suname = data["subject"]
		page = self.rooms[session["user"].uname]
		page.sync()
		usr = User.get({"uname" : suname}, {"class" : 1})
		lk = page.block(usr)
		page.save()
		emit("general", APIButtonChange(id="block", innerHTML=("Block" if lk else "Unblock")).toDict())
		print("blocked", ("Block" if lk else "Unblock"))
	
	def checkProfileStatus(self):
		messages = []
		user = session["user"]
		page = self.rooms[session["user"].uname]
		if not user.email_valid:
			messages.append("Your email has not yet been validated, please check your email")
		info = UserInfo.get({"_id" : user.details})
		if not (len(info.images) >= 1):
			messages.append("You need atleast 1 image on your profile")
		if (len(info.tags) < 5):
			messages.append("You need a minimum of 5 tags on your profile")
		if (len(info.biography) < 50):
			messages.append("Your biography must be atleast 50 characters long")
		if (info.gender == "Unknown"):
			messages.append("Please specify a gender")
		if messages:
			emit("accountStatus", APIException(message="<br>".join(messages), state=False, persist=True).toDict())
		if page.alerts:
			unread = page.getUnread()
			emit("notify", APISuccessMessage(message=unread, notify=len(unread)).toDict())
			pass

