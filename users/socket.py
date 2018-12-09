from flask_socketio import Namespace

class UserSockets(Namespace):
    def __init__(self):
        Namespace.__init__(self, "/user_socket_transactions")
    pass
