from app.obj import Page, Validator, User
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
        validation = self.validator.validate(data)
        if (validation['status'] is not Validator.VALID):
            return flask.jsonify(validation)
        usr = User()
        usr.parse_dbo(data)
        usr.log_fields()
        userok = usr.isValid()# Returns false if it is valid
        if(userok): 
            return flask.jsonify(userok)    
        
        return flask.jsonify(validation)


