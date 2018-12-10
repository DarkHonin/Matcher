from flask import Blueprint, render_template, abort, session
from users import requires_Users, user
from users.user_info import UserInfo
from api import APIMessageRecievedDecorator, APIException, APIMessage
from .messages import SettingsMessage, FieldUpdatedMessage
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
	return FieldUpdatedMessage(displayMessage="The setting has been saved", fields={option : updated}).messageSend()

########################################################################################################################################################
@ACCOUNTS_BLUEPRINT.route("/settings")
@requires_Users
def account_settings(user : user.User):
	info = UserInfo.get({"_id" : user.details})
	return render_template("account/pages/settings.html", user=user, info=info)
