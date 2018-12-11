from flask_socketio import Namespace, emit
from flask import session
from api import APIException
from .user_info import UserInfo
from .user import User

class UserSockets(Namespace):

    CONNECTED_USERS = {}

    def __init__(self):
        Namespace.__init__(self, "/user_socket_transactions")
    
    def on_connect(self):
        user = User.get({"_id" : session["user"]}, {"hash" : 0})
        print("user has come online :", user.uname)
        UserSockets.CONNECTED_USERS[str(user._id)] = user.loginToken
        emit("now_online", {"user" : user.uname}, broadcast=True)

    def on_disconnect(self):
        user = User.get({"_id" : session["user"]}, {"hash" : 0})
        if str(user._id) in UserSockets.CONNECTED_USERS:
            del(UserSockets.CONNECTED_USERS[str(user._id)])
            emit("now_offline", {"user" : user.uname}, broadcast=True)

    def on_accountStatus(self):
        messages = []
        user = User.get({"_id" : session["user"]}, {"hash" : 0})
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
            emit("accountStatus", APIException(message="<br>".join(messages)).toDict())
