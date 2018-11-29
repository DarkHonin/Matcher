from systems.users.user import User
from systems.users.user_info import UserInfo

def requires_Users(f):
	from functools import wraps
	from flask import session, redirect, url_for
	@wraps(f)
	def ParseSession(*args, **kws):
		if ("user" not in session) or ("user_info" not in session):
			return redirect(url_for("index", page="login"))
		user = User.from_dict(session['user'])
		info = UserInfo.from_dict(session['user_info'])
		return f(user, info)
	return ParseSession