from flask.views import MethodView
from flask import Flask, render_template, request, jsonify, redirect, url_for
from systems.properties import check_captcha, RequestValidator
from systems.exceptions import SystemException
from systems.users import User, UserInfo, requires_Users
from systems.tokens import redeemToken

from bson.objectid import ObjectId

class Home(MethodView):

	decorators = [requires_Users]

	def get(self, user : UserInfo):
		if not user:
			return redirect(url_for("logout"))
		if not user.info.complete:
			return redirect(url_for("settings"))
		elif user.info.complete and not user.active:
			user.activate()
		elif not user.active:
			return "There was a problem activating the account"
		tele = Telemetry.forUser(user)
		ids = [ObjectId(i) for i in tele.pageViews ]
		viewers = UserInfo.get({"_id" : {"$in" : ids}})
		if viewers:
			if not isinstance(viewers, list):
				viewers = [viewers]
		else:
			viewers = []

		return render_template("pages/user/home.html", user=user, tel=tele, viewers=viewers)

	@classmethod
	def bind(cls, app : Flask):
		app.add_url_rule("/home", view_func=cls.as_view("home"))
