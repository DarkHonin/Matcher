from app.obj import Page
from app.validator import *
from app.token import Token
from app.users import LoginUser
import flask

class TokenRedeem(Page):
    def __init__(self):
        Page.__init__(self, ["/token/<token>"], "Matcher::Welcome", methods=["GET", "POST"])
        self.validator = Validator(
            [
                PASSWORD_FIELD,
                UNAME_FIELD,
                Field("g-recaptcha-response", {"Captvha failed" : Validator.checkCaptcha}, True, "Captcha"),

            ]  
        )

    def get(self, token):
        return flask.render_template("pages/index/redeem.html", token=token)

    def post(self, token):
        data = flask.request.json
        if not self.validator.validate(data):
            return  flask.jsonify({"status" : "NOJOY", "message" : self.validator.ERROR})
        print("Data logged")
        token = Token.get(Token, {"token" : token})
        if(not token):
            return flask.jsonify({"status" : Validator.INVALID, "message" : "Your token is invalid"})
        user = token.resolve()
        if not LoginUser(user, data['password']):
            return flask.jsonify({"status" : "NOJOY", "message" : "Email/Password invalid"})
        token.delete()
        return flask.jsonify({"status" : Validator.VALID, "action" : "redirect", "message" : "/user"})