from app.obj import Page, Validator
from app.users import LoginUser
import flask

class Login(Page):
    def __init__(self):
        Page.__init__(self, ["/", "/login"], "Matcher::Welcome", methods=["GET", "POST"])
        self.validator = Validator(
            {
                "uname" : {"Can only contain alpha numeric values" : Validator.isAlphaNumeric, 
                            "Must be longer than 6 characters" : [Validator.isLonger, [6]]},
                "g-recaptcha-response" : {"Recaptcha failed" : Validator.checkCaptcha}
                }
        )

    def get(self):
        return flask.render_template("pages/index/login.html")

    def post(self):
        data = flask.request.json
        resp = {}
        if not self.validator.validate(data):
            return  flask.jsonify(self.validator.STATUS)
        print("Data logged")
        if not LoginUser(data, resp):
            return flask.jsonify(resp['error'])
        print("User Logged in")
        return flask.jsonify({"status" : Validator.VALID})