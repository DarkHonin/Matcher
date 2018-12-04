from flask.views import MethodView
from flask import Flask, render_template, request, jsonify, redirect, url_for
from systems.properties import check_captcha, RequestValidator
from systems.exceptions import SystemException
from systems.users import User, UserInfo, requires_Users
from systems.tokens import redeemToken


class Profile(MethodView):

	decorators = [requires_Users]

	def get(self, name, user):
		view_user = User.get({"uname" : name})
		if not view_user:
			return redirect(url_for("error", error="User does not exist"))
		if not view_user.active:
			return redirect(url_for("error", error="This user exists but has not been activated yet"))
		if user.active:
			user.telemetry.viewing(view_user)
			view_user.telemetry.view(user)
			view_user.save()
			user.save()
		return render_template("pages/user/profile.html", user=view_user)

	def post(self, name, user):
		view_user = UserInfo.get({"uname" : name})
		if not view_user:
			return redirect(url_for("error", error="User does not exist"))
		tele = Telemetry.forUser(view_user)
		cur_tel = Telemetry.forUser(user)
		if str(view_user._id) in cur_tel.likes:
			cur_tel.likes.remove(str(view_user._id))


	@classmethod
	def bind(cls, app : Flask):
		app.add_url_rule("/user/<name>", view_func=cls.as_view("user"), methods=["GET", "POST"])
