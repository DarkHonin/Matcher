from app.obj import Page
from app.validator import *
from app.users import LoginUser, LookupUser
import flask

class Login(Page):
    def __init__(self):
        Page.__init__(self, ["/", "/login"], "Matcher::Welcome", methods=["GET", "POST"])
        self.validator = Validator(
            [
                PASSWORD_FIELD,
                UNAME_FIELD,
                Field("g-recaptcha-response", {"Captvha failed" : Validator.checkCaptcha}, True, "Captcha"),
            ]  
        )

    def get(self):
        return flask.render_template("pages/index/login.html")

    def post(self):
        data = flask.request.json
        if not self.validator.validate(data):
            return  flask.jsonify({"status" : "NOJOY", "message" : self.validator.ERROR})
        print("Data logged")
        user = LookupUser(data["uname"])
        if not user:
            return flask.jsonify({"status" : "NOJOY", "message" : "Email/Password invalid"})
        if not LoginUser(user, data["password"]):
            return flask.jsonify({"status" : "NOJOY", "message" : "Email/Password invalid"})
        if(not user.active):
            return flask.jsonify({"status" : "NOJOY", "message" : "Please activate your acount first"})
        print("User Logged in")
        return flask.jsonify({"status" : Validator.VALID, "action" : "redirect", "message" : "/user"})