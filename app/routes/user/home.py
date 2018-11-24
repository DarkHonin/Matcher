from app.obj import Page
import flask

class Home(Page):
    def __init__(self):
        Page.__init__(self, "/home", "Matcher::Home", methods=["GET", "INFO"])

    def get(self):
        if("user" not in flask.session):
            return flask.redirect("/login")
        from app.users import User
        if not User.get(User, {"uid" : flask.session['user']}):
            return flask.redirect("/login")
        return flask.render_template("pages/user/home.html")

    def info(self):
        if("user" not in flask.session):
            return flask.redirect("/login")
        from app.users import User
        user = User.get(User, {"uid" : flask.session['user']})
        if not user:
            return flask.redirect("/login")

        from app.JSON_responce import JsonResponce
        resp = JsonResponce()
        if(not user.isComplete()):
            resp.action("displayMessage", "Please complete your profile", "NOJOY")
        # has messages waiting
        # or some shit
        return resp.render()
        
