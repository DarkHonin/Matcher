from flask_socketio import Namespace, emit
from flask import session
from systems.users import requires_Users

class SocketSystem(Namespace):

    CONNECTED_USERS = {}

    decorators = [requires_Users]

    def on_connect(self, user):
        SocketSystem.CONNECTED_USERS[session["user"]] = "Online"

    def on_disconnect(self, user):
        SocketSystem.CONECTED_USERS[session["user"]] = "Away"

    def on_getMessages(self, user):
        pass

    @staticmethod
    def getStatus(uid):
        if uid in SocketSystem.CONNECTED_USERS:
            return SocketSystem.CONNECTED_USERS[uid]
        return "Offline"


    @classmethod
    def bind(cls, app):
        from app import sockets
        sockets.on_namespace(SocketSystem('/user_transmissions'))

