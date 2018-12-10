from .user import User
from .user_info import UserInfo
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
