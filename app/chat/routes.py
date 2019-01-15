from flask import Blueprint
from flask_jwt_exteded import jwr_required

CHAT = Blueprint("chat", __name__)

@CHAR.route("/chat")
@jwt_required
def view():
    pass
