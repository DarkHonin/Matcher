from flask_jwt_extended import get_jwt_identity, jwt_optional, jwt_required
from flask import Blueprint, render_template, request, jsonify, make_response, url_for
from app.api.api import APIRedirectingException, APIMessageRecievedDecorator, APIException, APISuccessMessage
from app.users import User
from .api import OptionSet
from . import Account
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
from app.tokens import create_token
from app.database import Callback
from io import BytesIO
import base64

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
		if k == "gender" or k == "interest" or k == "lname" or k == "fname" or k == "biography":
			setattr(account, k, v)
			account.save()
		elif k == "uname":
			user.uname = v
			user.save()
		elif k == "password":
			user.password = generate_password_hash(v)
			user.save()
		elif k == "email":
			user.verified = False
			user.email = v
			create_token(user, Callback("verify_email", module="app.users", cls="User"))
			user.save()
		elif k == "tags":
			if not isinstance(v, list):
				raise APIException(message="Tags can only be submitted as an array")
			things = [x.lower() for x in v]
			setattr(account, k, list(set(things)))
			account.save()
		elif k == "image":
			if len(account.images) < 5:
				account.images.append(v)
				account.save()
			return APISuccessMessage(displayMessage={"message" : "Image uploaded"}, update={"insert" : ".options", "fn" : "userImage", "data" : {
				"src" : url_for("accounts.user_image", uid=user._id, id=len(account.images) - 1),
				"image_id" : len(account.images) - 1
				}}).messageSend()
		return "OK"

@ACCOUNT_BLUEPRINT.route("/settings/delimg/<id>", methods=["POST"])
@jwt_required
def delImg(id):
	ident = get_jwt_identity()
	account = Account.get({"user" : ObjectId(ident["id"])}, {"class" : 1, "images" : 1, "user": 1})
	del account.images[int(id)]
	return APISuccessMessage(displayMessage={"message" : "Image uploaded"}, remove={
																					"query" : "[src='/image/%s/%s']" % (account.user, id)
				}).messageSend()

@ACCOUNT_BLUEPRINT.route("/image/<uid>/<id>")
@jwt_required
def user_image(uid, id : int):
	get_jwt_identity()
	images = Account.get({"user" : ObjectId(uid)}, {"class" : 1, "images" : {"$slice" : [int(id), 1]}})
	if not images.images:
		raise APIException(message="Image does not exist")
	st = images.images.pop()
	mime = st[str(st).index(":") + 1: str(st).index(";")]
	byte = base64.b64decode(st[str(st).index(",")+1:])
	resp = make_response(byte)
	resp.headers.set('Content-Type', mime)
	return resp