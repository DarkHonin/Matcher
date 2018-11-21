from app.obj import Page, Validator, User
import flask

class Register(Page):
    def __init__(self):
        Page.__init__(self, [ "/register"], "Matcher::Welcome", methods=["GET", "POST"])
        self.validator = Validator(
            {
                "fname" : {"Is not a valid name" : Validator.isValidName},
                "lname" : {"Is not a valid name" : Validator.isValidName},
                "uname" : {"Can only contain alpha numeric values" : Validator.isAlphaNumeric, 
                            "Must be longer than 6 characters" : [Validator.isLonger, [6]]}
                
                }
        )

    def get(self):
        return flask.render_template("pages/index/register.html")

    def post(self):
        data = flask.request.json
        validation = self.validator.validate(data)
        if (validation['status'] is not Validator.VALID):
            return flask.jsonify(validation)
        usr = User()
        usr.parse_dbo(data)
        usr.log_fields() 
        exc = usr.save()
        if (exc):
            return flask.jsonify(exc)
        return flask.jsonify(validation)


