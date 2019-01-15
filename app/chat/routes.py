from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, current_user
from .dbo import Chat

CHAT = Blueprint("chat", __name__)

@CHAT.route("/chat")
@jwt_required
def view():
    ownChats = pendingChats = Chat.get({"authors" : {"$elemMatch" : {"user" : current_user._id, "pending" : True}}})
    if not ownChats:
        ownChats = []
    else:
        if not isinstance(ownChats, list):
            ownChats = [ownChats]
    return render_template("alerts/pages/chat.html", ownChats=ownChats)
