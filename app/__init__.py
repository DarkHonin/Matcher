from api import APIException
from flask import Flask, jsonify, render_template, request, session, send_from_directory
from flask_mail import Mail
from flask_pymongo import PyMongo
from flask_socketio import SocketIO
from database import DBDDecoder, DBDEncoder
from users import USER_BLUEPRINT
from accounts import ACCOUNTS_BLUEPRINT
from messageing.Sockets import MessageSockets

APP = Flask(__name__)
APP.secret_key = "5bf87554084b104d3f7dbb52"
APP.config.from_pyfile("instance/config.py")
SOCKETS = SocketIO(APP)

print("Loading Routes")
APP.register_blueprint(USER_BLUEPRINT)
print("--User routes loaded")
APP.register_blueprint(ACCOUNTS_BLUEPRINT)
print("--Account routes loaded")
SOCKETS.on_namespace(MessageSockets())

DATABASE = PyMongo(APP)
MAILER = Mail(APP)

@APP.errorhandler(APIException)
def handle_error(error : APIException):
    return error.messageSend(), 500

APP.json_encoder = DBDEncoder
APP.json_decoder = DBDDecoder

@APP.route("/image/<fn>")
def getUserImage(fn):
	return send_from_directory("static/uploads/", fn)

@APP.route("/error/?e='<error>'&r='<ret>'")
def error(error, ret):
    return render_template("error.html", error=error, ret=ret)

@APP.route("/bogus")
def bogus():
    import app.bogus.load_bogus
    return "Bogus users loaded"

def resolve_user(id):
    from users import User
    return User.get({"_id" : id})

def resolve_info(id):
    from users.profile import Profile
    return Profile.get({"_id" : id})

APP.jinja_env.globals.update(resolve_user=resolve_user)
APP.jinja_env.globals.update(resolve_info=resolve_info)

"""
@APP.route("/error/<error>")
def error(error):
    return render_template("pages/error.html", err=error, txt=error[:2].upper())

from views import VIEWS
for view in VIEWS:
    print("Binding %s" % view)
    view.bind(APP)

@APP.route("/test")
def test():
    from systems.users import registerUser, User
    #registerUser("Username", "email@email.com", "First", "Last", "Passw0rd")
    return jsonify(User.get())

@APP.route("/testEncode")
def endode():
    from systems.users import registerUser, User
    item = User.get()[0]
    item.telemetry.postMessage("A test", 0)
    item.save()
    return jsonify(item.encodeDocument())

"""
