from flask.views import MethodView
from flask import Flask, render_template, request, jsonify, redirect, url_for
from systems.properties import check_captcha, RequestValidator
from systems.exceptions import SystemException
from systems.users import User, UserInfo, requires_Users
from systems.tokens import redeemToken

from bson.objectid import ObjectId

class Home(MethodView):

	decorators = [requires_Users]

	def get(self, user : User):
		if not user:
			return redirect(url_for("logout"))
		return render_template("pages/user/home.html", user=user)

	@classmethod
	def bind(cls, app : Flask):
		app.add_url_rule("/home", view_func=cls.as_view("home"))
