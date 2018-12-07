from systems.users.user import User
from systems.users.user_info import UserInfo
from systems.users.chat import Chat, CHAT_ACCEPTED, CHAT_PENDING
from systems.exceptions import SystemException
from systems.telemetry import Telemetry
from flask import session

def requires_Users(f):
	from functools import wraps
	from flask import session, redirect, url_for
	import datetime
	@wraps(f)
	def ParseSession(*args, **kws):
		print("Resolveing current user")
		if ("user" not in session):
			return redirect(url_for("error", error="You are no longer logged in", callback="login"))
		return f(user=session["user"], *args, **kws)
	return ParseSession

def registerUser(uname, email, fname, lname, password, dob):
	user = User(uname, email)
	user.password = password
	user.info = UserInfo(fname, lname)
	user.info._dob = dob
	user.telemetry = Telemetry()
	user.register()
	return user

def setProp(data, subject):
	field = subject.fields[int(data['id'])]
	field.validate(data)
	subject.__setattr__(field.key, data[field.key])


