from app.obj import Page, Validator
from app.token import Token
from app.users import LoginUser
import flask

class TokenRedeem(Page):
    def __init__(self):
        Page.__init__(self, ["/token/<token>"], "Matcher::Welcome", methods=["GET", "POST"])
        self.validator = Validator(
            {
                "uname" : {"Can only contain alpha numeric values" : Validator.isAlphaNumeric, 
                            "Must be longer than 6 characters" : [Validator.isLonger, [6]]},
                "g-recaptcha-response" : {"Recaptcha failed" : Validator.checkCaptcha}
                }
        )

    def get(self, token):
        return flask.render_template("pages/index/redeem.html", token=token)

    def post(self, token):
        data = flask.request.json
        resp = {}
        if not self.validator.validate(data):
            return  flask.jsonify(self.validator.STATUS)
        print("Data logged")
        if not LoginUser(data, resp) or 'error' in resp:
            return flask.jsonify(resp['error'])
        print("User Logged in")
        token = Token.get(Token, {"token" : token})
        if(not token):
            return flask.jsonify({"status" : Validator.INVALID, "message" : "Your token is invalid"})
        token.resolve()
        return flask.jsonify({"status" : Validator.VALID})