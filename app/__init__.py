from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from .api import APIException, APIRedirectingException
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO

APP = Flask(__name__)							#Create app instnce
APP.config.from_pyfile("instance/config.py")	#Config file load

DATABASE = PyMongo(APP)							#Create database connection
EMAIL_CLIENT = Mail(APP)						#Create email client
SOCKET = SocketIO(APP)

#########################################################
#####	App spesific routes		#########################
#########################################################

@APP.errorhandler(APIException)
def handle_error(error : APIException):
    return error.messageSend(), 500

@APP.errorhandler(APIRedirectingException)
def render_redirect_exception(err : APIRedirectingException):
	return render_template("error.html", error=err.displayMessage["message"], redirect=err.redirect["location"], label=err.actionLabel)

from .users.routes import USER_BLUEPRINT
from .tokens.routes import TOKEN_BLUEPRINT
from .account.routes import ACCOUNT_BLUEPRINT
from .search.routes import SEARCH_BLUEPRINT
from .notifications.socket import Notifier

SOCKET.on_namespace(Notifier())

APP.register_blueprint(USER_BLUEPRINT)
APP.register_blueprint(TOKEN_BLUEPRINT)
APP.register_blueprint(ACCOUNT_BLUEPRINT)
APP.register_blueprint(SEARCH_BLUEPRINT)

JSONWT = JWTManager(APP)

@JSONWT.user_identity_loader
def user_identity_lookup(user):
    return {"id" : str(user._id)}

@JSONWT.user_loader_callback_loader
def user_loader_callback(identity):
	from .users import User
	return User.get({"_id" : identity["id"]})

@JSONWT.expired_token_loader
def my_expired_token_callback():
	if request.method == "POST":
		return APIException(message="Your login has expired, please login again").messageSend(), 401
	return render_redirect_exception(APIRedirectingException(redirect="users.login", displayMessage={"message" : "Your login has expired, please login again"}, actionLabel="Login"))

def resolve_user(id):
    from .users import User
    return User.get({"_id" : id})

def resolve_account(id):
	from .account import Account
	print(">>>",{"thing" : id})
	return Account.get({"user" : id})

APP.jinja_env.globals.update(resolve_user=resolve_user)
APP.jinja_env.globals.update(resolve_account=resolve_account)