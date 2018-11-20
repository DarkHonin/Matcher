from app.obj import Page
import flask

class Login(Page):
    def __init__(self):
        Page.__init__(self, ["/", "/login"], "Matcher::Welcome", methods=["GET"])

    def get(self):
        return flask.render_template("pages/index/login.html")

