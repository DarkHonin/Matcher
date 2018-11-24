from app.obj import Page
from app.users import RegisterUser, User
from app.validator import *
import flask
from app.JSON_responce import JsonResponce

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
        resp = JsonResponce()
        if not RegisterUser(user, data['password']):
            resp.action("displayMessage", user.ERROR, "NOJOY")
        else:
            resp.action("displayMessage" , "An activation email has been sent!")
        return resp.render()


