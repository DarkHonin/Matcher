from systems.users.user import User
from systems.users.user_info import UserInfo
from systems.users.telemetry import Telemetry
from systems.exceptions import SystemException
from flask import session

def requires_Users(f):
	from functools import wraps
	from flask import session, redirect, url_for
	import datetime
	@wraps(f)
	def ParseSession(*args, **kws):
		print("Resolveing current user")
		if ("user" not in session):
			return redirect(url_for("error", error="You are no longer logged in"))
		user = User.get({"_id": session['user']})
		if not user:
			del(session['user'])
			return redirect(url_for("error", error="Your session has expired, please login again"))
		user.last_online = datetime.datetime.now()
		user.save()
		return f(user=user, *args, **kws)
	return ParseSession

def registerUser(uname, email, fname, lname, password):
	user = User(uname, email)
	user.password = password
	user.info = UserInfo(fname, lname)
	user.telemetry = Telemetry()
	user.register()
	return user

def setProp(data, subject):
	field = subject.fields[int(data['id'])]
	field.validate(data)
	subject.__setattr__(field.key, data[field.key])


