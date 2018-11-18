from app.obj import Page
import flask

class Index(Page):
    def __init__(self):
        super(Index, self).__init__("/", "Matcher::Index")

    def get(self):
        return flask.render_template("components/index/login.html")
