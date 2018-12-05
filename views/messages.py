from flask.views import MethodView
from flask import Flask, render_template, request, jsonify, redirect, url_for
from systems.properties import check_captcha, RequestValidator
from systems.exceptions import SystemException
from systems.users import User, UserInfo, requires_Users
from systems.tokens import redeemToken


class Messages(MethodView):

	decorators = [requires_Users]

	def get(self, user):
		return render_template("pages/messages/alerts.html", user=user)

	def fetch(self, user):
		unread = 0
		display = []
		for i in user.telemetry.notifications:
			if not i.read:
				unread += 1
			if not i.displayed:
				display.append(i.display)

		actions = {
			"unread" : unread,
			"displayMessage" : "<br>".join(display)
			}
		user.save()
		return jsonify({"status" : "JOY", "actions" : actions})


	@classmethod
	def bind(cls, app : Flask):
		app.add_url_rule("/notify", view_func=cls.as_view("messages"), methods=["FETCH", "GET"])
