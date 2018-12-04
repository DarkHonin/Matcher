from flask.views import MethodView
from flask import Flask, render_template, request, jsonify, redirect, url_for
from systems.properties import check_captcha, RequestValidator
from systems.exceptions import SystemException
from systems.users import User, UserInfo, requires_Users
from systems.tokens import redeemToken


class Messages(MethodView):

	decorators = [requires_Users]

	def get(self, name, user):
		view_user = User.get({"uname" : name})
		if not view_user:
			return redirect(url_for("error", error="User does not exist"))
		if not view_user.active:
			return redirect(url_for("error", error="This user exists but has not been activated yet"))
		if user.active:
			view_user.telemetry.view(user)
			view_user.save()
		return render_template("pages/user/profile.html", user=view_user)

	def fetch(self, user):
		unread = 0
		display = []
		for i in user.telemetry.notifications:
			if not i["read"]:
				unread += 1
			if not i['displayed']:
				display.append(i["message"])
				i["displayed"] = True

		if not display:
			return jsonify({"status" : "NOJOY"})
		ret = jsonify({
			"status" : "JOY",
			"actions" : {
				"displayMessage" : "<br>".join(display),
				"unreadCount"	 : unread
			}
		})
		user.save()
		return ret


	@classmethod
	def bind(cls, app : Flask):
		app.add_url_rule("/messages", view_func=cls.as_view("messages"), methods=["GET", "FETCH"])
