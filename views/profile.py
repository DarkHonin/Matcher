from flask.views import MethodView
from flask import Flask, render_template, request, jsonify, redirect, url_for
from systems.properties import check_captcha, RequestValidator
from systems.exceptions import SystemException
from systems.users import User, UserInfo, requires_Users
from systems.tokens import redeemToken
from systems.telemetry import _telemetry

class Profile(MethodView):

	decorators = [requires_Users]

	def get(self, name, user):
		user_page = User.get({"uname" : name})
		if not user_page:
			return redirect(url_for("error", error="User '%s' does not exist" % name))
		if not user_page.active:
			return redirect(url_for("error", error="This user exists but has not been activated yet"))
		telemetry = _telemetry(user)
		telemetry2 = _telemetry(user_page)
		if user_page._id in telemetry._blocked:
			return render_template("pages/user/unblock.html", user=user_page)
		if user._id in telemetry2._blocked:
			return redirect(url_for("error", error="This user has blocked you"))
		if user.active:
			telemetry.isViewing(user_page)
			telemetry2.wasViewedBy(user)
			telemetry.save()
			telemetry2.save()
		return render_template("pages/user/profile.html", user=user_page, current_user=user, telemetry=telemetry2)

	def like(self, name, user):
		view_user = User.get({"uname" : name})
		if not view_user:
			return jsonify({"status" : "NOJOY", "actions" : {"displayMessage": "The user does not exist"}})
		if not view_user.active:
			return jsonify({"status" : "NOJOY", "actions" : {"displayMessage": "You can not like an unactivated user"}})
		if user.active:
			Telemetry.like(user, view_user)
			return jsonify({"status" : "JOY", "actions" : {"displayMessage": "You have %s %s" % (("liked" if user.telemetry.likes(view_user) else "unliked"), name), "updateLikeButton" : ("Like" if not user.telemetry.likes(view_user) else "Unlike")}})
		return jsonify({"status" : "NOJOY", "actions" : {"displayMessage": "Your accont needs to be active to like users"}})

	def block(self, name, user):
		view_user = User.get({"uname" : name})
		if not view_user:
			return jsonify({"status" : "NOJOY", "actions" : {"displayMessage": "The user does not exist"}})
		if not view_user.active:
			return jsonify({"status" : "NOJOY", "actions" : {"displayMessage": "You can not block an unactivated user"}})
		user.telemetry.block(view_user)
		user.save()
		return jsonify({"status" : "JOY", "actions" : {"displayMessage": "This user has now been blocked", "redirect" : url_for("user", name=name)}})

	def unblock(self, name, user):
		view_user = User.get({"uname" : name})
		if not view_user:
			return jsonify({"status" : "NOJOY", "actions" : {"displayMessage": "The user does not exist"}})
		user.telemetry._blocked.remove(view_user._id)
		user.save()
		return jsonify({"status" : "JOY", "actions" : {"displayMessage": "This user has now been unblocked", "redirect" : url_for("user", name=name)}})

	@classmethod
	def bind(cls, APP : Flask):
		APP.add_url_rule("/user/<name>", view_func=cls.as_view("user"), methods=["GET", "LIKE", "BLOCK", "UNBLOCK"])
