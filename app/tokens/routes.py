from flask import Blueprint, request, render_template, url_for
from . import User
from . import Token
from app.users.api import APIInvalidUser
from .api import APIInvalidToken
from app.users.api import LoginMessage
from app.api import APIMessageRecievedDecorator, APIValidatingMessage, APIException, APISuccessMessage
from app.account import create_user_account
from flask_jwt_extended import set_access_cookies, set_refresh_cookies, create_access_token, create_refresh_token

TOKEN_BLUEPRINT = Blueprint("tokens", __name__)

@TOKEN_BLUEPRINT.route("/redeem/<token>", methods=["GET", "POST"])
@TOKEN_BLUEPRINT.route("/redeem/", methods=["GET", "POST"])
@APIMessageRecievedDecorator(LoginMessage)
def redeem(message : APIValidatingMessage, token=None):
	if request.method == "GET":
		return render_template("users/pages/redeem.html", submit_to=url_for("tokens.redeem"))
	elif request.method == "POST":
		message.validate()
		if not message.valid:
			raise message.errorMessage
		_token = Token.get({"token" : token})
		if not _token:
			raise APIInvalidToken()
		user = User.get({"uname" : message.uname})
		if not user or user._id != _token.resource:
			raise APIInvalidUser()
		resp = APISuccessMessage(displayMessage={"message" : "Your token has been redeemed"}, redirect="accounts.settings").messageSend()
		user.login(message.password, resp)
		_token.redeem()(user)
		return resp