from flask import Blueprint, render_template, abort
from users import requires_Users, user
from users.user_info import UserInfo
from api import APIMessageRecievedDecorator, APIException
from .messages import SettingsMessage
ACCOUNTS_BLUEPRINT = Blueprint("user_accounts", __name__)

########################################################################################################################################################

@ACCOUNTS_BLUEPRINT.route("/settings/<option>", methods=["POST"])
@requires_Users
@APIMessageRecievedDecorator(SettingsMessage)
def set_user_attribute(option, user : user.User, message:SettingsMessage):
	if not message.valid:
		raise message.errorMessage
	info = UserInfo.get({"_id" : user.details})
	if not hasattr(user, option) or not hasattr(info, option):
		raise APIException(message="The field '%s' is not a valid propery" % option)
	return "heck"

########################################################################################################################################################
@ACCOUNTS_BLUEPRINT.route("/settings")
@requires_Users
def account_settings(user : user.User):
	info = UserInfo.get({"_id" : user.details})
	return render_template("account/pages/settings.html", user=user, info=info)
