from flask.views import MethodView
from flask import Flask, render_template, request, jsonify, redirect, url_for
from systems.properties import check_captcha, RequestValidator
from systems.exceptions import SystemException
from systems.users import User, UserInfo, requires_Users
from systems.tokens import redeemToken
from systems.telemetry import Telemetry

class Profile(MethodView):

	def get(self, name):
		user = UserInfo.get({"uname" : name})
		tele = Telemetry.forUser(user)
		if (tele):
			tele.pageViews += 1
			tele.save()
		return render_template("pages/user/profile.html", user=user, tel=tele)

	@classmethod
	def bind(cls, app : Flask):
		app.add_url_rule("/user/<name>", view_func=cls.as_view("user"))
