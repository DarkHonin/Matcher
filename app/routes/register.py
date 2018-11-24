from app.obj import Page
from app.users import RegisterUser, User
from app.validator import *
import flask

class Register(Page):
    def __init__(self):
        Page.__init__(self, [ "/register"], "Matcher::Welcome", methods=["GET", "POST"])
        self.validator = Validator(
            [
                EMAIL_FIELD,
                PASSWORD_FIELD,
                Field("fname", {"Not a valid first name" : Validator.isValidName}, True, "First name"),
                Field("lname", {"Not a valid last name" : Validator.isValidName}, True, "Lirst name"),
                UNAME_FIELD,
                Field("g-recaptcha-response", {"Captvha failed" : Validator.checkCaptcha}, True, "Captcha")
            ]  
        )

    def get(self):
        return flask.render_template("pages/index/register.html")

    def post(self):
        data = flask.request.json
        if not self.validator.validate(data):
            return  flask.jsonify({"status" : "NOJOY", "message" : self.validator.ERROR})
        print("Data logged")
        user = User()
        user.parse_dbo(data)
        if not RegisterUser(user, data['password']):
            return flask.jsonify(user.ERROR)
        """
        print("User registered")
        return flask.jsonify({"status" : Validator.VALID, "message" : "Your account has been registered, please verify your email", "action" : "display"})
        """
        return flask.jsonify({"status" : "JOY"})


