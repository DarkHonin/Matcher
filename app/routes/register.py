from app.obj import Page, Validator
import flask

class Register(Page):
    def __init__(self):
        Page.__init__(self, [ "/register"], "Matcher::Welcome", methods=["GET", "POST"])
        self.validator = Validator(
            {
                "fname" : [Validator.isValidName],
                "lname" : [Validator.isValidName],
                "uname" : [Validator.isAlphaNumeric, [Validator.isLonger, [6]]]
                
                }
        )

    def get(self):
        return flask.render_template("pages/index/register.html")

    def post(self):
        data = flask.request.json
        return flask.jsonify(self.validator.validate(data))

