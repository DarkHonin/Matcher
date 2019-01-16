from flask_socketio import Namespace, join_room, emit
from flask_jwt_extended import decode_token
from .dbo import Chat, Message
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
		print("%s::%s connected to chat" % (current_user._id, current_user.uname))

	def prepare_messages(self, messages):
		current_user = self.current_user
		ret = []
		for i in messages:
			ret.append(
				{"user" : str(i.author),
				"message" : i.message,
				"time" : str(i.time)
				}
			)
		print(ret)
		return ret

	def on_get_messages(self, id):
		chat = Chat.get({"_id":ObjectId(id["id"])})
		for i in chat.authors:
			if not i["pending"]:
				return emit("chat_pending", {"chat_id" : id["id"]})
		join_room(str(chat._id))
		emit("show_chat", {"messages" : self.prepare_messages(chat.messages), "chat_id" : id["id"]})

	def on_message_send(self, message, chat_id):
		current_user = self.current_user
		ms = Message(current_user._id, message)
		chat = Chat.get({"_id":ObjectId(chat_id)})
		chat.messages.append(ms)
		chat.save()
		emit("message_get", {"message" : {"user" : str(current_user._id),
				"message" : ms.message,
				"time" : str(ms.time)
				}}, room=str(chat._id), broadcast=True)