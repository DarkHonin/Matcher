from systems.users.user import User
from systems.users.user_info import UserInfo
from systems.exceptions import SystemException
from systems.telemetry import Telemetry
from flask import session

def requires_Users(f):
	from functools import wraps
	from flask import session, redirect, url_for
	@wraps(f)
	def ParseSession(*args, **kws):
		if ("user" not in session):
			return redirect(url_for("index", page="login"))
		user = UserInfo.get({"_id": session['user']})
		return f(user)
	return ParseSession

def registerUser(uname, email, fname, lname, password):
	user = UserInfo(fname, lname, password=password, uname=uname, email=email)
	return user

def setProp(data, subject):
	for i in ["key", "id"]:
		if i not in data:
			raise SystemException("Invalid field selection", SystemException.FIELD_ERROR)
	field = subject.fields[int(data['id'])]
	field.validate(data)
	subject.__setattr__(field.key, data[field.key])
	if subject.active:
		i = Telemetry.forUser(subject).handle(data['key'], data[int(data['id'])])
		i.save()
		subject.save()
	else:
		if subject.complete:
			i = Telemetry(subject)
			i.handle(data['key'], data[int(data['id'])])
			i.save()
			subject.activate()


