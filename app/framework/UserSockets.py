import uuid
from flask_sockets import Sockets
class UserSocketsHandler:

	INSTANCE = None
	SOCKETS = None

	def __init__(self, app):
		print("Loading websocket handler")
		self.SOCKETS = Sockets(app)
		self.SOCKETS.add_url_rule("/home","usersocet", self.handle)
		self.INSTANCE = self
		self.authTokens = []
		self.connections = {}
		print("Loaded")

	def createToken(self):
		id = uuid.uuid1().hex
		self.authTokens.append(id)
		return id

	def handle(self, ws):
		message = ws.receive()
		import json
		from app.JSON_responce import JsonResponce
		qda = JsonResponce()
		js = json.loads(message)
		for a, d in js.items():
			fn = self.__getattribute__(a)
			if(fn):
				fn(qda, d)
		ws.send(str({"status" : qda.state, "actions": qda.actions}))

	def connect(self, resp, token):
		from app.users import User, GetCurrentUser
		obj = GetCurrentUser()
		if not obj:
			resp.action("display", "Invalid user/token, please login again", "NOJOY")
		if(token not in self.authTokens):
			resp.action("display", "Invalid user/token, please login again", "NOJOY")
		if(token in self.authTokens):
			self.connections[id] = obj
			self.authTokens.remove(token)
			

			

	