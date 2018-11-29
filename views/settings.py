from flask.views import MethodView
from flask import Flask, render_template, request, jsonify, session
from systems.properties import check_captcha, RequestValidator
from systems.exceptions import SystemException
from systems.users import User, UserInfo, requires_Users
from systems.tokens import redeemToken

class Settings(MethodView):

	decorators = [check_captcha, requires_Users]

	def get(self, user, info):
		return render_template("pages/user/settings.html", info=info, user=user)

	def post(self, user : User, info : UserInfo):
		data = request.get_json()
		for i in ["key", "item", "id"]:
			if i not in data:
				raise SystemException("Invalid field selection", SystemException.FIELD_ERROR)
		if data['item'] == "user":
			subject = user
		elif data['item'] == "info":
			subject = info
		field = subject.fields[int(data['id'])]
		field.validate(data)
		subject.__setattr__(field.key, data[field.key])
		subject.save()
		session['user'] = dict(user)
		session['user_info'] = dict(info)
		return jsonify({"status" : "JOY", "actions" : {"displayMessage" : "The field has been saved"}})
			
	@classmethod
	def bind(cls, app : Flask):
		app.add_url_rule("/settings", view_func=cls.as_view("settings"))
		
