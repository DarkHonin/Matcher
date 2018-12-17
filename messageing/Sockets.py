from flask_socketio import Namespace, emit, join_room, leave_room
from flask import session
from users.page import Page
from database import DBDocument
import datetime
from users import User, Profile
from api import APISuccessMessage, APIException, APIMessage
from uuid import uuid4

class APIButtonChange(APIMessage):
	pass

class MessageSockets(Namespace):
	

	INSTANCE = None

	def __init__(self):
		Namespace.__init__(self, "/messages")
		self.rooms = {}
		MessageSockets.INSTANCE = self

	def on_connect(self):
		if session["user"] not in self.rooms:
			self.rooms[str(session["user"])] = {
				"user" : User.get({"_id" : session["user"]}, {"hash" : 0}),
				"profile" : Profile.get({"user" : session["user"]}),
				"room" : uuid4()
			}
		data = self.rooms[str(session["user"])]
		print("user has come online :", data["user"].uname)
		join_room(data["room"])
		emit("now_online", {"user" : data["user"].uname}, broadcast=True)

	def on_disconnect(self):
		if session["user"] not in self.rooms:
			return
		leave_room(session["user"].uname)
		print("user now offline :", self.rooms[session["user"]].user.uname)
		emit("now_offline", {"user" : self.rooms[session["user"]].user.uname}, broadcast=True)

	@staticmethod
	def sendMessage(user : User, message : str):
		from app import APP, SOCKETS
		with APP.app_context():
			if str(user._id) in MessageSockets.INSTANCE.rooms:
				room = MessageSockets.INSTANCE.rooms[str(user._id)]["room"]
				print("Emmiting to room ", room)
				SOCKETS.emit("accountStatus", APISuccessMessage(message=message).toDict(), room=room, namespace="/messages")

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
