from app.obj import Page, Validator
from app.users import RegisterUser
import flask

class Register(Page):
    def __init__(self):
        Page.__init__(self, [ "/register"], "Matcher::Welcome", methods=["GET", "POST"])
        self.validator = Validator(
            {
                "fname" : {"Is not a valid name" : Validator.isValidName},
                "lname" : {"Is not a valid name" : Validator.isValidName},
                "uname" : {"Can only contain alpha numeric values" : Validator.isAlphaNumeric, 
                            "Must be longer than 6 characters" : [Validator.isLonger, [6]]},
                "email" : {"Must be a valid email" : Validator.isEmail},
                "g-recaptcha-response" : {"Recaptcha failed" : Validator.checkCaptcha}
                }
        )

    def get(self):
        return flask.render_template("pages/index/register.html")

    def post(self):
        data = flask.request.json
        resp = {}
        if not self.validator.validate(data):
            return  flask.jsonify(self.validator.STATUS)
        print("Data logged")
        if not RegisterUser(data, resp):
            return flask.jsonify(resp['error'])
        print("User registered")
        return flask.jsonify({"status" : Validator.VALID})


