from flask.views import MethodView
from flask import Flask, render_template, request, jsonify, session, url_for, send_from_directory
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

	def insert(self, user : User, info : UserInfo):
		data = request.get_json()
		if info.imageCount == 5:
			raise SystemException("You may not have more than 5 images", SystemException.FIELD_ERROR)
		if 'data' not in data:
			raise SystemException("No image to read", SystemException.FIELD_ERROR)
		image_64 = data['data']
		if not str(image_64).startswith("data:image/jpeg;base64,"):
			raise SystemException("Invalid image", SystemException.FIELD_ERROR)
		import base64
		from datetime import datetime
		from app import app
		import os
		from werkzeug.utils import secure_filename
		image_64 = str(image_64).replace("data:image/jpeg;base64,", "")
		bins = base64.b64decode(image_64)
		date = datetime.now()
		fn = "%s_%s_%s_%s_%s_%s.jpg" % (date.year, date.month, date.hour, date.minute, date.second, user._id)
		fd = open(os.path.join(app.config['UPLOAD_FOLDER'], fn) , "wb+")
		fd.write(bins)
		fd.close()
		info.images.append(fn)
		info.save()
		session['user_info'] = dict(info)
		return jsonify({"status" : "JOY", "actions" : {"displayMessage" : "Image uploaded", "insertImage":url_for("getUserImage", fn=fn)}})

	@classmethod
	def bind(cls, app : Flask):
		app.add_url_rule("/settings", view_func=cls.as_view("settings"), methods=["GET", "POST", "INSERT"])
		@app.route("/image/<fn>")
		def getUserImage(fn):
			return send_from_directory("static/uploads/", fn)
		

		
