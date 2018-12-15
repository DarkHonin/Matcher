from .socket import UserSockets
from .routes import USER_BLUEPRINT
from .user import User
USER_SOCKET = UserSockets()

CURRENT_USER = None

def requires_Users(f):
	from functools import wraps
	from flask import session, redirect, url_for
	import datetime
	@wraps(f)
	def ParseSession(*args, **kws):
		print("Resolveing current user")
		if ("user" not in session):
			return redirect(url_for("error", error="You are no longer logged in", ret="user_manager.login"))
		if (not user):
			return redirect(url_for("error", error="You are no longer logged in", ret="user_manager.login"))
		return f(user=session["user"], *args, **kws)
	return ParseSession