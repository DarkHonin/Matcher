from flask.views import MethodView
from flask import Flask, render_template, request, jsonify, redirect, url_for
from systems.properties import check_captcha, RequestValidator
from systems.exceptions import SystemException
from systems.users import User, UserInfo, requires_Users
from systems.tokens import redeemToken
from systems.telemetry import Telemetry

class Home(MethodView):

	decorators = [requires_Users]

	def get(self, user : UserInfo):
		if not user:
			return redirect(url_for("logout"))
		if not user.complete:
			return redirect(url_for("settings"))
		elif user.complete and not user.active:
			user.activate()
		elif not user.active:
			return "There was a problem activating the account"
		tele = Telemetry.forUser(user)
		return render_template("pages/user/home.html", user=user, tel=tele)

	@classmethod
	def bind(cls, app : Flask):
		app.add_url_rule("/home", view_func=cls.as_view("home"))
