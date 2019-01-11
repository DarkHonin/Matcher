from flask_jwt_extended import get_jwt_identity, jwt_optional, jwt_required, current_user
from flask import Blueprint, render_template, request, jsonify, make_response, url_for
from app.api.api import APIRedirectingException, APIMessageRecievedDecorator, APIException, APISuccessMessage
from app.users import User
from .api import OptionSet
from . import Account, Telemetry
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
from app.tokens import create_token
from app.database import Callback
from io import BytesIO
import base64

ACCOUNT_BLUEPRINT = Blueprint("accounts", __name__)

@ACCOUNT_BLUEPRINT.route("/settings", methods=["GET", "POST"])
@jwt_required
@APIMessageRecievedDecorator(OptionSet)
def settings(message : OptionSet):
	print(current_user)
	if not current_user:
		raise APIRedirectingException(redirect="users.login", displayMessage={"message" : "You must first login to view this page"}, actionLabel="Login")
	account = Account.get({"user" : ObjectId(current_user._id)})
	if request.method == "GET":
		return render_template("account/pages/settings.html", user=current_user, info=account)
	if request.method == "POST":
		message.validate()
		if not message.valid:
			raise message.errorMessage
		k, v = message.setting
		if k == "gender" or k == "interest" or k == "lname" or k == "fname" or k == "biography":
			setattr(account, k, v)
			account.save()
		elif k == "uname":
			current_user.uname = v
			current_user.save()
		elif k == "password":
			current_user.password = generate_password_hash(v)
			current_user.save()
		elif k == "email":
			current_user.verified = False
			current_user.email = v
			create_token(current_user, Callback("verify_email", module="app.users", cls="User"))
			current_user.save()
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
			return APISuccessMessage(displayMessage={"message" : "Image uploaded"}, update={"action" : "insert","subject" : ".options", "before" : ".usr_img.add", "fn" : "userImage", "data" : {
				"src" : url_for("accounts.user_image", uid=current_user._id, id=len(account.images) - 1),
				"image_id" : len(account.images) - 1
				}}).messageSend()
		return "OK"

@ACCOUNT_BLUEPRINT.route("/profile/<uid>")
@jwt_required
def public_profile(uid):
	id = ObjectId(uid)
	profile_user = User.get({"_id" : id})
	profile_telemetry = Telemetry.get({"user" : id})
	view_tel = Telemetry.get({"user" : current_user._id})
	account = Account.get({"user" : id})
	if not current_user._id == id:
		profile_telemetry.view(current_user)
		profile_telemetry.save()
	return render_template("account/pages/profile.html", user=profile_user, viewer=current_user, account=account, telemetry=profile_telemetry, showMeta=current_user._id == id, viewer_telemetry=view_tel)
	

@ACCOUNT_BLUEPRINT.route("/profile")
@jwt_required
def private_profile():
	account = Account.get({"user" : current_user._id})
	telemetry = Telemetry.get({"user" : current_user._id})
	return render_template("account/pages/profile.html", user=current_user, account=account, telemetry=telemetry, showMeta=True)

@ACCOUNT_BLUEPRINT.route("/settings/delimg/<id>", methods=["POST"])
@jwt_required
def delImg(id):
	col = Account.collection()
	print(col.update_one({"user" : current_user._id}, {"$unset" : {"images."+id : 1}}).raw_result)
	print(col.update_one({"user" : current_user._id}, {"$pull" : {"images" : None}}).raw_result)
	return APISuccessMessage(displayMessage={"message" : "Deleted image"}, update={"action" : "remove",
	"subject" : ".usr_img[image_id='%s']" % id}).messageSend()

@ACCOUNT_BLUEPRINT.route("/image/<uid>/<id>")
@jwt_required
def user_image(uid, id : int):
	images = Account.get({"user" : ObjectId(uid)}, {"class" : 1, "images" : {"$slice" : [int(id), 1]}})
	if not images.images:
		raise APIException(message="Image does not exist")
	st = images.images.pop()
	mime = st[str(st).index(":") + 1: str(st).index(";")]
	byte = base64.b64decode(st[str(st).index(",")+1:])
	resp = make_response(byte)
	resp.headers.set('Content-Type', mime)
	return resp

@ACCOUNT_BLUEPRINT.route("/profile/<uid>/<action>", methods=["POST"])
@jwt_required
def action_thing(uid, action):
	if ObjectId(uid) == current_user._id:
		raise APIException(message="You cant Like, Block or report yourself")
	if action == "like":
		tel = Telemetry.get({"user" : ObjectId(uid)})
		tel.like(current_user)
		tel.save()
		return APISuccessMessage(displayMessage={"message" : "Liked"}, update={"action" : "replace",
			"subject" : "#like", "fn" : "has_been_liked"}).messageSend()
	elif action == "block":
		from app import resolve_user
		blocked = resolve_user(ObjectId(uid))
		ttl = Telemetry.get({"user" : current_user._id})
		ttl.block(blocked)
		ttl.save()
		return APISuccessMessage(displayMessage={
			"message" : "This user is now %s" % ( "blocked" if blocked._id in ttl.blocked else "unblocked")}, 
			update={
				"action" : "change",
				"subject" : "#block", 
				"fn" : "blocking", 
				"data": "%s" %("Block" if not blocked._id in ttl.blocked else "Unblock") 
			}).messageSend()
	elif action == "report":
		#Something or the other, need to think about this
		
		pass
	else:
		raise APIException(message="Invalid option")
	return "OK"
	