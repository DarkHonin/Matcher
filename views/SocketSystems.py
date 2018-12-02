from flask_socketio import Namespace, emit
from flask import session

class SocketSystem(Namespace):

    CONNECTED_USERS = {}

    def on_connect(self):
        if session["user"] not in SocketSystem.CONNECTED_USERS:
            SocketSystem.CONNECTED_USERS[session["user"]] = "Online"

    def on_disconnect(self):
        SocketSystem.CONNECTED_USERS[session["user"]] = "Away"

    @staticmethod
    def getStatus(uid):
        if uid in SocketSystem.CONNECTED_USERS:
            return SocketSystem.CONNECTED_USERS[uid]
        return "Offline"


    @classmethod
    def bind(cls, app):
        from app import sockets
        sockets.on_namespace(SocketSystem('/user_transmissions'))

