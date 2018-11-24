from app.obj import Page
import flask

class User(Page):
    def __init__(self):
        super(User, self).__init__(["/user", "/user/<uname>"], "Matcher::User")

    def get(self):
        if("user" not in flask.session):
            return flask.redirect("/")
        
        from app.users import User
        user = User.get(User, {"uid" : flask.session['user']})
        if not user:
            return flask.redirect("/")
        return flask.render_template("pages/user/landing.html", user=user)
