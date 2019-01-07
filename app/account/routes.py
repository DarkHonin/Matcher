from flask_jwt_extended import get_jwt_identity, jwt_optional
from flask import Blueprint, render_template, request, jsonify
from app.api.api import APIRedirectingException, APIMessageRecievedDecorator, APIException
from app.users import User
from .api import OptionSet
from . import Account
from bson.objectid import ObjectId

ACCOUNT_BLUEPRINT = Blueprint("accounts", __name__)

@ACCOUNT_BLUEPRINT.route("/settings", methods=["GET", "POST"])
@jwt_optional
@APIMessageRecievedDecorator(OptionSet)
def settings(message : OptionSet):
	ident = get_jwt_identity()
	if not ident:
		raise APIRedirectingException(redirect="users.login", displayMessage={"message" : "You must first login to view this page"}, actionLabel="Login")
	user = User.get({"_id" : ObjectId(ident["id"])})
	account = Account.get({"user" : ObjectId(ident["id"])})
	if request.method == "GET":
		return render_template("account/pages/settings.html", user=user, info=account)
	if request.method == "POST":
		message.validate()
		if not message.valid:
			raise message.errorMessage
		k, v = message.setting
		if k == "gender":
			pass
		elif k == "uname":
			pass
		elif k == "password":
			pass
		elif k == "email":
			pass
		elif k == "lname" or k == "fname":
			pass
		elif k == "tags":
			pass
		return "OK"