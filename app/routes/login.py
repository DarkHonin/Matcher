from app.obj import Page
from app.validator import *
from app.users import LoginUser, LookupUser
from app.JSON_responce import JsonResponce
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
        if("user" in flask.session):
            return flask.redirect(flask.url_for("home_GET"))
        return flask.render_template("pages/index/login.html")

    def post(self):
        data = flask.request.json
        if not self.validator.validate(data):
            return  flask.jsonify({"status" : "NOJOY", "message" : self.validator.ERROR})
        print("Data logged")
        user = LookupUser(data["uname"])
        responce = JsonResponce()
        if not LoginUser(user, data["password"]) or not user.active:
            responce.action("displayMessage" , "Email/Password invalid", "NOJOY")
        else:
            responce.action("displayMessage" , ("Welcome back %s" % (user.uname)))
            responce.action("redirect" , "/home")
            print("User Logged in")
        return responce.render()