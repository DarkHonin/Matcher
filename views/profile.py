from flask.views import MethodView
from flask import Flask, render_template, request, jsonify, redirect, url_for
from systems.properties import check_captcha, RequestValidator
from systems.exceptions import SystemException
from systems.users import User, UserInfo, requires_Users, Telemetry
from systems.tokens import redeemToken


class Profile(MethodView):

	decorators = [requires_Users]

	def get(self, name, user):
		user_page = User.get({"uname" : name})
		if not user_page:
			return redirect(url_for("error", error="User does not exist"))
		if not user_page.active:
			return redirect(url_for("error", error="This user exists but has not been activated yet"))
		if user.active:
			Telemetry.view(user_page, user)
		return render_template("pages/user/profile.html", user=user_page, current_user=user)

	def like(self, name, user):
		view_user = User.get({"uname" : name})
		if not view_user:
			return redirect(url_for("error", error="User does not exist"))
		if not view_user.active:
			return redirect(url_for("error", error="This user exists but has not been activated yet"))
		if user.active:
			Telemetry.like(user, view_user)
			return jsonify({"status" : "JOY", "actions" : {"displayMessage": "You have %s %s" % (("liked" if user.telemetry.likes(view_user) else "unliked"), name), "updateLikeButton" : ("Like" if not user.telemetry.likes(view_user) else "Unlike")}})
		return jsonify({"status" : "NOJOY", "actions" : {"displayMessage": "Your accont needs to be active to like users"}})



	@classmethod
	def bind(cls, app : Flask):
		app.add_url_rule("/user/<name>", view_func=cls.as_view("user"), methods=["GET", "LIKE"])
