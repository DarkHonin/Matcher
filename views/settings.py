from flask.views import MethodView
from flask import Flask, render_template, request, jsonify, session, url_for, send_from_directory, redirect
from systems.properties import check_captcha, RequestValidator
from systems.exceptions import SystemException
from systems.users import User, UserInfo, requires_Users, setProp
from systems.tokens import redeemToken

class Settings(MethodView):

	decorators = [check_captcha, requires_Users]

	def get(self, user : UserInfo):
		if not user:
			return redirect(url_for("logout"))
		return render_template("pages/user/settings.html", user=user)

	def post(self, user : User):
		data = request.get_json()
		for i in ["key", "id", "item"]:
			if i not in data:
				raise SystemException("Invalid field selection", SystemException.FIELD_ERROR)
		if data["item"] == "user":
			setProp(data, user)
		elif data['item'] == "info":
			setProp(data, user.info)
		else:
			raise SystemException("Invalid field selection", SystemException.FIELD_ERROR)
		user.activate()
		session["user"] = user
		return jsonify({"status" : "JOY", "actions" : {"displayMessage" : "The field has been saved"}})

	def insert(self, user : User):
		data = request.get_json()
		if user.info.imageCount == 5:
			raise SystemException("You may not have more than 5 images", SystemException.FIELD_ERROR)
		if 'data' not in data:
			raise SystemException("No image to read", SystemException.FIELD_ERROR)
		image_64 = data['data']
		if not str(image_64).startswith("data:image/jpeg;base64,"):
			raise SystemException("Invalid image", SystemException.FIELD_ERROR)
		import base64
		from datetime import datetime
		from APP import APP
		import os
		from werkzeug.utils import secure_filename
		image_64 = str(image_64).replace("data:image/jpeg;base64,", "")
		bins = base64.b64decode(image_64)
		date = datetime.now()
		fn = "%s_%s_%s_%s_%s_%s.jpg" % (date.year, date.month, date.hour, date.minute, date.second, user._id)
		fd = open(os.path.join(APP.config['UPLOAD_FOLDER'], fn) , "wb+")
		fd.write(bins)
		fd.close()
		user.info.images.append(fn)
		user.save()
		session["user"] = user
		return jsonify({"status" : "JOY", "actions" : {"displayMessage" : "Image uploaded", "insertImage":url_for("getUserImage", fn=fn)}})

	@classmethod
	def bind(cls, APP : Flask):
		APP.add_url_rule("/settings", view_func=cls.as_view("settings"), methods=["GET", "POST", "INSERT"])
		
		

		
