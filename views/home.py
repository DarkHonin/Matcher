from flask.views import MethodView
from flask import Flask, render_template, request, jsonify, redirect, url_for
from systems.properties import check_captcha, RequestValidator
from systems.exceptions import SystemException
from systems.users import User, UserInfo, requires_Users
from systems.tokens import redeemToken
from systems.telemetry import Telemetry

class Home(MethodView):

	decorators = [requires_Users]

	def get(self, info : UserInfo):
		if not info:
			return redirect(url_for("logout"))
		if not info.complete:
			return redirect(url_for("settings"))
		elif info.complete and not info.active:
			info.activate()
		elif not info.active:
			return "There was a problem activating the account"
		tele = Telemetry.forUser(info)
		return render_template("pages/user/home.html", user=info, tel=tele)

	@classmethod
	def bind(cls, app : Flask):
		app.add_url_rule("/home", view_func=cls.as_view("home"))
