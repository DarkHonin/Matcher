from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from .api import APIException, APIRedirectingException
from flask_mail import Mail
from flask_jwt_extended import JWTManager

APP = Flask(__name__)							#Create app instnce
APP.config.from_pyfile("instance/config.py")	#Config file load

DATABASE = PyMongo(APP)							#Create database connection
EMAIL_CLIENT = Mail(APP)						#Create email client

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

APP.register_blueprint(USER_BLUEPRINT)
APP.register_blueprint(TOKEN_BLUEPRINT)
APP.register_blueprint(ACCOUNT_BLUEPRINT)

JSONWT = JWTManager(APP)

@JSONWT.expired_token_loader
def my_expired_token_callback():
	if request.method == "POST":
		return APIException(message="Your login has expired, please login again").messageSend(), 401
	return render_redirect_exception(APIRedirectingException(redirect="users.login", displayMessage={"message" : "Your login has expired, please login again"}, actionLabel="Login"))