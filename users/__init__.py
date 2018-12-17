from .socket import UserSockets
from .routes import USER_BLUEPRINT
from .user import User
from .profile import Profile
from .page import Page
USER_SOCKET = UserSockets()

def requires_Users(f):
	from functools import wraps
	from flask import session, redirect, url_for
	import datetime
	@wraps(f)
	def ParseSession(*args, **kws):
		print("Resolveing current user")
		if ("user" not in session):
			return redirect(url_for("error", error="You are no longer logged in", ret="user_manager.login"))
		user = User.get({"_id" : session["user"]}, {"hash" : 0})
		if (not user):
			return redirect(url_for("error", error="You are no longer logged in", ret="user_manager.login"))
		return f(user=user, *args, **kws)
	return ParseSession

def requires_Profile(f):
	from functools import wraps
	from flask import session, redirect, url_for
	import datetime
	@wraps(f)
	def ParseSession(*args, **kws):
		usr = kws.pop("profile")
		if usr is None:
			user = kws["user"]
		else:
			user = User.get({"uname" : usr}, {"hash" : 0})
		if not user:
			return redirect(url_for("error", error="The user '%s' does not exist" % usr, ret="user_accounts.account_profile"))
		profile = Profile.get({"user" : user._id})
		return f(profile=profile, view_user=user, *args, **kws)
	return ParseSession

def requires_Page(f):
	from functools import wraps
	from flask import session, redirect, url_for
	import datetime
	@wraps(f)
	def ParseSession(*args, **kws):
		if "profile" not in kws:
			return redirect(url_for("error", error="The users page is not ready yet", ret="user_accounts.account_profile"))
		profile = kws["profile"]
		complete, errs = profile.complete()
		if not complete:
			print(errs)
			return redirect(url_for("error", error="The users page is not complete yet", ret="user_accounts.account_profile"))
		page = Page.get({"user":kws["view_user"]._id})
		if not page:
			page = Page(kws["view_user"])
			page.save()
		return f(page=page, *args, **kws)
	return ParseSession