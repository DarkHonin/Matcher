from flask.views import MethodView
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from systems.properties import check_captcha, RequestValidator
from systems.exceptions import SystemException
from systems.users import User, UserInfo, requires_Users, Chat, CHAT_PENDING
from flask_socketio import Namespace, emit
import datetime

class UserStatus:
	def __init__(self):
		self.lastCheckIn = datetime.datetime.now()

	def checkIn(self):
		self.lastCheckIn = datetime.datetime.now()

	def status(self):
		if not self.lastCheckIn:
			return -1
		delta = datetime.datetime.now() - self.lastCheckIn
		if delta > datetime.timedelta(minutes=15):
			return 0
		if delta > datetime.timedelta(minutes=30):
			return -1
		return 1

class Messages(Namespace, MethodView):

	decorators = [requires_Users]

	ONLINE_USERS = {}

	def get(self, user):
		if request.path == "/notify":
			return render_template("pages/messages/alerts.html", user=user)
		if request.path == "/chat":
			chats = Chat.get({"users.chatState"  : CHAT_PENDING, "users.uid" : user._id})
			if not isinstance(chats, list) and chats:
				chats = [chats]
			return render_template("pages/messages/chat.html", user=user, chats=chats)

	def getSessionUser(self, telemetry : bool=False):
		if "user" not in session:
			return None
		if not telemetry:
			return User.get({"_id" : session['user']}, {
				"token" : 1, 
				"class" : 1,
				})
		else:
			return User.get({"_id" : session['user']}, {
				"token" : 1, 
				"class" : 1,
				"telemetry" : 1
				})

	def on_connect(self):
		print("Connected")

	def on_init(self, data):
		if "token" not in data:
			emit("general_socket_handle", {"actions" : {"displayMessage" : "Socket init requires a valid token"}})
		usr = self.getSessionUser()
		if not usr:
			emit("general_socket_handle", {"actions" : {"displayMessage" : "You need to have a valid session to get messages"}})
		token = data.pop("token")
		if token != usr.token:
			emit("general_socket_handle", {"actions" : {"displayMessage" : "Invalid socket token"}})
		Messages.ONLINE_USERS[usr._id] = UserStatus()
		emit("general_socket_handle", {"actions" : {"displayMessage" : "Messages now connected"}})
		emit("start_requests")

	def on_getMessages(self):
		user = self.getSessionUser(True)
		if user._id not in self.ONLINE_USERS:
			emit("general_socket_handle", {"actions" : {"displayMessage" : "This socket connection is not authed"}})
		unread = 0
		display = []
		for i in user.telemetry.notifications:
			if not i.read:
				unread += 1
			if not i.displayed:
				display.append(i.display)

		chats = Chat.get({"users.chatState"  : CHAT_PENDING, "users.uid" : user._id}, {"_id" : 1})
		if not isinstance(chats, list) and chats:
			chats = [chats]
		actions = {
			"unread" : unread,
			"displayMessage" : "<br>".join(display),
			"pendingChats" : len(chats) if chats else 0
			}
		if display:
			user.save()
		emit("general_socket_handle", {"actions" : actions})
		
	def accept(self, user):
		data = request.get_json()
		from bson.objectid import ObjectId
		from systems.users import CHAT_ACCEPTED
		if "chat" not in data:
			return jsonify({"status" : "NOJOY", "actions" : {"displayMessage" : "Could not complete query"}})
		chat = Chat.get({"_id" : ObjectId(data['chat'])}, {"class" : 1, "users" : 1})
		if not chat:
			return jsonify({"status" : "NOJOY", "actions" : {"displayMessage" : "Could not find chat"}})
		for i in chat.users:
			if i.uid == user._id:
				i.chatState = CHAT_ACCEPTED
		chat.save()
		return jsonify({"status" : "JOY"})
		

	@classmethod
	def bind(cls, app : Flask):
		from app import sockets
		sockets.on_namespace(Messages('/messages'))
		app.add_url_rule("/notify", view_func=cls.as_view("messages"))
		app.add_url_rule("/chat", view_func=cls.as_view("chat"), methods=["ACCEPT", "REGECT", "GET"])
