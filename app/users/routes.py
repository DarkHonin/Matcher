from flask import Blueprint, request, render_template, url_for, make_response, jsonify, redirect, session
from . import User
from .api import RegisterMessage, LoginMessage, APIInvalidUser, APIUserNotActive
from app.api import APIMessageRecievedDecorator, APIValidatingMessage, APIException, APISuccessMessage
from app.account import create_user_account
from app.tokens import create_token
from flask_jwt_extended import unset_access_cookies, unset_refresh_cookies, jwt_required, get_current_user
from app.database import Callback


USER_BLUEPRINT = Blueprint("users", __name__)

@USER_BLUEPRINT.route("/generate_random_users")
def make_bogus():
	from bogus import load_bogus
	return "Users have been loaded"

@USER_BLUEPRINT.route("/register", methods=["GET", "POST"])
@APIMessageRecievedDecorator(RegisterMessage)
def register(message : RegisterMessage):
	if request.method == "GET":
		return render_template("users/pages/register.html")
	elif request.method == "POST":
		message.validate()
		if not message.valid:
			raise message.errorMessage
		user = User(**message.__dict__)
		user.save()
		try:
			create_token(user, Callback("activate_account", module="app.users", cls="User"))
		except APIException as e:
			user.delete()
			raise e
		create_user_account(user, message)
		ret = APISuccessMessage(redirect="users.login", display_message="Redirecting to login page")
		return ret.messageSend()

@USER_BLUEPRINT.route("/login", methods=["GET", "POST"])
@USER_BLUEPRINT.route("/", methods=["GET", "POST"])
@APIMessageRecievedDecorator(LoginMessage)
def login(message : LoginMessage):
	if request.method == "GET":
		return render_template("users/pages/login.html", submit_to=url_for("users.login"))
	if request.method == "POST":
		message.validate()
		if not message.valid:
			raise message.errorMessage
		user = User.get({"uname" : message.uname})
		if not user:
			raise APIInvalidUser()
		if not user.active:
			raise APIUserNotActive()
		resp = APISuccessMessage(displayMessage={"message" : "You are now logged in"}, redirect="accounts.private_profile").messageSend()
		session["token"] = user.login(message.password, resp)
		return resp


@USER_BLUEPRINT.route("/logout", methods=["GET", "POST"])
def logout():
	resp = make_response(redirect(url_for("users.login")))
	unset_access_cookies(resp)
	unset_refresh_cookies(resp)
	return resp