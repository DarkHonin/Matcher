from flask.views import MethodView
from flask import Flask, render_template, request, jsonify, redirect, url_for
from systems.properties import check_captcha, RequestValidator
from systems.exceptions import SystemException
from systems.users import User, UserInfo, requires_Users
from systems.tokens import redeemToken
from bson.objectid import ObjectId
from systems.telemetry import _telemetry

class Home(MethodView):

	decorators = [requires_Users]

	def get(self, user : User):
		telemetry = _telemetry(user)
		return render_template("pages/user/home.html", user=user, telemetry=telemetry)

	def meta(self, user):
		data = request.get_json()
		if "tag" not in data:
			return jsonify({"status" : "NOJOY"})
		actions = {"page_views" : user.telemetry.viewers, "view_history" : user.telemetry.viewHistory, "liked_users": user.telemetry.getLikes}
		if data['tag'] not in actions:
			return jsonify({"status" : "NOJOY"})
		return jsonify({"status" : "JOY", "items" : actions[data['tag']]()})
	

	@classmethod
	def bind(cls, app : Flask):
		app.add_url_rule("/home", view_func=cls.as_view("home"), methods=["GET", "META"])
