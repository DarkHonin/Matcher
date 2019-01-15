from flask_socketio import Namespace, join_room
from flask_jwt_extended import decode_token
from .dbo import Chat
from flask import session
from bson import ObjectId

class ChatSpace(Namespace):

	ONLINE = []

	def __init__(self):
		Namespace.__init__(self, "/chat")

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
		print("%s::%s connected to chat" % (current_user._id, current_user.uname))

	def on_get_messages(self, id):
		current_user = self.current_user
		chat = Chat.get_for_ids(ObjectId(id["id"]), current_user._id)
		print(chat)