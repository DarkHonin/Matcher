from flask_socketio import Namespace, join_room, emit, leave_room
from flask_jwt_extended import decode_token
from .dbo import Chat, Message
from flask import session
from bson import ObjectId

class ChatSpace(Namespace):

	ONLINE = {}

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
		print("%s::%s connected to chat" % (current_user._id, current_user.uname))
		unread = []
		unread_chats = Chat.get_unread(current_user._id)
		if unread_chats:
			for q in unread_chats:
				unread.append({
					"chat_id" : str(q._id),
					"count" : q.unread_count(current_user._id)
				})
		emit("unread_chats", unread)

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

	def on_get_messages(self, id):
		print("get messages")
		chat = Chat.get({"_id":ObjectId(id["id"])})
		for i in chat.authors:
			if not i["pending"]:
				return emit("chat_pending", {"chat_id" : id["id"]})
		if "current_chat" in session:
			leave_room(session["current_chat"])
		join_room(str(chat._id))
		session["current_chat"] = str(chat._id)
		emit("show_chat", {"messages" : self.prepare_messages(chat.messages), "chat_id" : id["id"]})
		from app.notifications.socket import Notifier
		current_user = self.current_user
		Notifier.push_chat_count(current_user._id, chat)

	def on_message_send(self, message, chat_id):
		print("message sent")
		if not message:
			return 
		current_user = self.current_user
		ms = Message(current_user._id, message)
		chat = Chat.get({"_id":ObjectId(chat_id)})
		chat.messages.append(ms)
		chat.save()
		from app.notifications.socket import Notifier
		Notifier.push_message_count(chat.get_other_user(current_user._id), len(Chat.get_unread(chat.get_other_user(current_user._id))))
		emit("message_get", {"message" : {"user" : str(current_user._id),
				"message" : ms.message,
				"time" : str(ms.time)
				}}, room=str(chat._id), broadcast=True)
		Notifier.push_chat_count(chat.get_other_user(current_user._id), chat)

	def on_read(self, chat_id):
		print("chat read")
		chat = Chat.get({"_id" : ObjectId(chat_id)})
		current_user = self.current_user
		for q in chat.messages:
			if q.author != current_user._id and not q.read:
				q.read = True
		chat.save()
		from app.notifications.socket import Notifier
		Unread_chats = Chat.get_unread(current_user._id)
		Notifier.push_message_count(current_user._id, len(Unread_chats))
		Notifier.push_chat_count(current_user._id, chat)
		