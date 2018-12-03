from flask.views import MethodView
from flask import Flask, render_template, request, jsonify
from systems.properties import check_captcha, RequestValidator
from systems.exceptions import SystemException
from systems.users import User
from systems.tokens import redeemToken

class Redeem(MethodView):

	decorators = [check_captcha, RequestValidator("/redeem")]

	def get(self, token=None):
		return render_template("pages/index/redeem.html", token=token)

	def post(self, token, uname, password):
		usr = User.get({"uname" : uname})
		if not usr:
			raise SystemException("Username/Password invalid", SystemException.USER_CREATE_EXCEPTION)
		usr.login(password)
		redeemToken(token)
		return jsonify({"status" : "JOY", "actions" : {"displayMessage" : "Your account is now active", "redirect" : "/home"}})		

	@classmethod
	def bind(cls, app : Flask):
		app.add_url_rule("/redeem/<token>", view_func=cls.as_view("redeem"))
