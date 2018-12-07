from systems.properties.property import Property
from systems.exceptions import SystemException
from functools import wraps
from flask import request

USERNAME = Property("uname", "Username", r"^[a-zA-Z0-9]{5,10}$", "The username can only be alphanumerical and between 5 and 10 characters", required=True)
EMAIL = Property("email", "Email", r"^[a-zA-Z0-9_\.\-]+@[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+$", "Please enter a valid email", required=True)
FIRSTNAME = Property("fname", "Firstname", r"^[A-Z][a-z]+$", "A name must start with one capital letter and is only alphabetical", required=True)
LASTNAME = Property("lname", "Lastname", r"^[A-Z][a-z]+$", "A name must start with one capital letter and is only alphabetical", required=True)
PASSWORD = Property("password", "Password", r"^(?=.*[A-Z])(?=.*\d)(?=.*[a-z]).{6,20}$", "A password must contain atleast one uppercase, lowecase and numeric character", required=True, fieldtype="password")
GENDER = Property("gender", "Gender", r"(Male|Female|Unset)", "Invalid gender, look, we dont really mind what you identify as but to others it matters whats inbetween your legs", fieldtype="enum")
INTEREST = Property("interest", "Interested in", r"(Men|Women|Both)", "Its cool that youre into that but we cant have that on record, you understand", fieldtype="enum")
TAGS = Property("tags", "Profile tags", r"^[^\<\>\{\}]+$", "Your tags may not look suspicios", fieldtype="list")
BIOGRAPHY = Property("biography", "Biography", r"^[^\<\>\{\}]+$", "Your tags may not look suspicios", fieldtype="blob")
DOB = Property("dob", "Date of birth", r".*", "Please supply a propper date", fieldtype="date")

class RequestValidator:

    FIELDS = {
        "/login" : [
            USERNAME,
            PASSWORD
        ],
        "/redeem" : [
            USERNAME,
            PASSWORD
        ],
        "/register" : [
            USERNAME,
            EMAIL,
            FIRSTNAME,
            LASTNAME,
            PASSWORD,
            DOB
        ]
    }

    def __init__(self, expliciteIndex=None):
        self.explicite = expliciteIndex

    def getFormName(self, data):
        if "form_name" not in data:
            raise SystemException("Invalid form context, please try again", SystemException.FIELD_ERROR)
        if data["form_name"] not in self.FIELDS:
            raise SystemException("Invalid form context, please try again", SystemException.FIELD_ERROR)
        return data["form_name"]

    def __call__(self, f):
        @wraps(f)
        def ValidateFields(*args, **kws):
            if(request.method != 'POST'):
                return f(*args, **kws)
            if self.explicite:
                page = self.explicite
            else:
                page = request.path
            data = request.get_json()
            fields = RequestValidator.FIELDS[page]
            pas = {}
            for field in fields:
                if hasattr(RequestValidator, field.key):
                    getattr(RequestValidator, field.key)(field, data)
                field.validate(data)
                pas[field.key] = data[field.key]
            return f(*args, **pas, **kws)
        return ValidateFields

    @staticmethod
    def dob(field, data:dict):
        dob = data.get("dob")
        print(dob)
        if not dob:
            raise SystemException("Invalid date of birth", SystemException.FIELD_ERROR)
        from datetime import datetime
        try:
            delta = datetime.now().year - datetime.strptime(dob, "%Y-%m-%d").year
            if delta < 18:
                raise SystemException("You must be atleast 18 or older", SystemException.FIELD_ERROR)
        except SystemException as e:
            raise e        
        except Exception as e:
            raise SystemException("The date was not propperly formatted", SystemException.FIELD_ERROR)

def check_captcha(f):
    from systems.exceptions import SystemException
    from app import app
    @wraps(f)
    def ValidateCaptcha(*args, **kws):
        if(request.method != 'POST'):
            return f(*args, **kws)
        data = request.get_json()
        if "g-recaptcha-response" not in data:
            raise SystemException("Invalid captcha, please try again", SystemException.FIELD_ERROR)
        if app.config.get("CAPTCHA_DISABLE"):
            print("captcha is disabled")
            return f(*args, **kws)
        import requests
        import json
        secret = app.config.get("CAPTCHA_SECRET")
        payload = {'response':data.pop("g-recaptcha-response"), 'secret':secret}
        try:
            response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
        except requests.exceptions.ConnectionError:
            raise SystemException("Failed to comunicate with captcha servers", SystemException.FIELD_ERROR)
        response_text = json.loads(response.text)
        if not response_text['success']:
            raise SystemException("Invalid captcha, please try again", SystemException.FIELD_ERROR)
        return f(*args, **kws)
    return ValidateCaptcha