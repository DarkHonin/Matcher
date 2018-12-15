from flask import Blueprint, render_template, abort, session, redirect, url_for
from users import requires_Users, user, User
from users.user_info import UserInfo
from api import APIMessageRecievedDecorator, APIException, APIMessage
from .messages import SettingsMessage, FieldUpdatedMessage
from users.page import Page
from messages.message import MessageSockets, message

ACCOUNTS_BLUEPRINT = Blueprint("user_accounts", __name__)



########################################################################################################################################################

@ACCOUNTS_BLUEPRINT.route("/settings/<option>", methods=["POST"])
@requires_Users
@APIMessageRecievedDecorator(SettingsMessage)
def set_user_attribute(option, user : user.User, message:SettingsMessage):
	ALLOWED = ["fname", "lname", "uname", "password", "email", "gender", "interest", "biography"]
	if not message.valid:
		raise message.errorMessage
	if not (hasattr(message, option)):
		raise APIException(message="The field '%s' is not a valid propery" % option)
	info = UserInfo.get({"_id" : user.details})
	if hasattr(info, "set_"+option):
		updated = getattr(info, "set_"+option)(getattr(message, option))
		info.save()
	elif hasattr(user, option):
		updated = getattr(user, "set_"+option)(getattr(message, option))
		user.save()
	else:
		raise APIException(message="The field '%s' is not a valid propery" % option)
	return FieldUpdatedMessage(displayMessage={"message":"The setting has been saved"}, fields={option : updated}).messageSend()

########################################################################################################################################################
@ACCOUNTS_BLUEPRINT.route("/settings")
@requires_Users
def account_settings(user : user.User):
	info = UserInfo.get({"_id" : user.details})
	return render_template("account/pages/settings.html", user=user, info=info)



@ACCOUNTS_BLUEPRINT.route("/p/<profile>", methods=["GET"])
@ACCOUNTS_BLUEPRINT.route("/home", defaults={"profile" : None}, methods=["GET"])
@requires_Users
def account_profile(user : user.User, profile):
	showMeta = user.uname != profile and profile
	if profile:
		usr = User.get({"uname" : profile}, {"hash" : 0})
		if not usr:
			return redirect(url_for("error", error="The user does not exist", ret="user_accounts.account_profile"))
	else:
		usr = user
	info = UserInfo.get({"_id" : usr.details})
	page = Page.get({"_id" : usr.page})
	if profile:
		if page.view(user):
			MessageSockets.INSTANCE.sendMessage(usr, "%s has just viewed your page" % user.uname)
			page.save()
	print(len(page.viewed_by))
	return render_template("account/pages/profile.html", user=usr, info=info, showMeta=showMeta, page=page)


@ACCOUNTS_BLUEPRINT.route("/p/<profile>", methods=["LIKE"])
@requires_Users
def like(user : user.User, profile):
	usr = User.get({"uname" : profile}, {"hash" : 0})
	page = Page.get({"_id" : usr.page})
	ret = APIButtonChange(id="like", innerHTML=("Like" if page.like(user) else "Unlike")).messageSend()
	#page.save()
	MessageSockets.INSTANCE.sendMessage(usr, message("Hellow there"))
	return ret
