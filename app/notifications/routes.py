from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, current_user
import time
NOTIFICATION = Blueprint("notifications", __name__)

@NOTIFICATION.route("/notifications")
@jwt_required
def notif():
	from app.notifications import UserNotifications
	alerts = UserNotifications.get_unread(current_user)
	for i in alerts:
		i.read = True
		i.save()
	return render_template("alerts/pages/alerts.html",alerts=alerts)

@NOTIFICATION.route("/messages")
def messages():
	pass


@NOTIFICATION.route("/notifications/older")
@jwt_required
def old_notif():
	from app.notifications import UserNotifications
	alerts = UserNotifications.get_read(current_user)
	return render_template("alerts/pages/alerts.html",alerts=alerts, old=True)
