from app.obj import Page
import flask

class Profile(Page):
    def __init__(self):
        Page.__init__(self, ["/user", "/user/<uname>"], "Matcher::User")

    def get(self, uname=None):
        if("user" not in flask.session):
            return flask.redirect("/login")
        user_current = False
        from app.users import User, LookupUser
        if(uname):
            user = LookupUser(uname)
        else:
            user = User.get(User, {"uid" : flask.session['user']})
            user_current = True
        if not user:
            return flask.redirect("/")
        if(user_current and (flask.request.args.get("edit"))):
            return flask.render_template("pages/user/profile_edit.html", user=user, user_current=user_current)    
        return flask.render_template("pages/user/profile.html", user=user, user_current=user_current)
