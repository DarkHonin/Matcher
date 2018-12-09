from flask import Blueprint

USER_BLUEPRINT = Blueprint("user_manager", __name__)


def requires_Users(f):
	from functools import wraps
	from flask import session, redirect, url_for
	import datetime
	@wraps(f)
	def ParseSession(*args, **kws):
		print("Resolveing current user")
		if ("user" not in session):
			return redirect(url_for("error", error="You are no longer logged in", callback="user_manager.login"))
		user = session["user"]
		if not user.verify():
			return redirect(url_for("error", error="You are no longer logged in", callback="user_manager.login"))
		return f(user=session["user"], *args, **kws)
	return ParseSession