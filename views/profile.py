from flask.views import MethodView
from flask import Flask, render_template, request, jsonify, redirect, url_for
from systems.properties import check_captcha, RequestValidator
from systems.exceptions import SystemException
from systems.users import User, UserInfo, requires_Users
from systems.tokens import redeemToken
from systems.telemetry import Telemetry

class Profile(MethodView):

	decorators = [requires_Users]

	def get(self, name, user):
		view_user = UserInfo.get({"uname" : name})
		if not view_user:
			return redirect(url_for("error", error="User does not exist"))
		tele = Telemetry.forUser(view_user)
		if (tele):
			if (str(user._id) not in tele.pageViews and view_user.uname != user.uname):
				tele.pageViews.append(str(user._id))
				tele.save()
		return render_template("pages/user/profile.html", user=view_user, tel=tele)

	@classmethod
	def bind(cls, app : Flask):
		app.add_url_rule("/user/<name>", view_func=cls.as_view("user"))
