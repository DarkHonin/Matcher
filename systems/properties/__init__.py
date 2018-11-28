from systems.properties.property import Property
from functools import wraps
from flask import request

USERNAME = Property("uname", "Username", r"^[a-zA-Z0-9]{5,10}$", "The username can only be alphanumerical and between 5 and 10 characters", required=True)
EMAIL = Property("email", "Email", r"^[a-zA-Z0-9_\.\-]+@[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+$", "Please enter a valid email", required=True)
FIRSTNAME = Property("fname", "Firstname", r"^[A-Z][a-z]+$", "A name must start with one capital letter and is only alphabetical", required=True)
LASTNAME = Property("lname", "Lastname", r"^[A-Z][a-z]+$", "A name must start with one capital letter and is only alphabetical", required=True)

FIELDS = {
    "/login" : [
        USERNAME
    ],
    "/register" : [
        USERNAME,
        EMAIL,
        FIRSTNAME,
        LASTNAME
    ]
}


def validate_request(f):
    @wraps(f)
    def ValidateFields(**kws):
        if(request.method != 'POST'):
            return f(**kws)
        page = request.path
        data = request.get_json()
        fields = FIELDS[page]
        for field in fields:
            field.validate(data)
        return f(**kws)
    return ValidateFields

def check_captcha(f):
    from systems.exceptions import SystemException
    from app import app
    @wraps(f)
    def ValidateFields(**kws):
        if(request.method != 'POST') or app.config.get("CAPTCHA_DISABLE"):
            return f(**kws)
        data = request.get_json()
        if "g-recaptcha-response" not in data:
            raise SystemException("Invalid captcha, please try again", SystemException.FIELD_ERROR)
        import requests
        import json
        secret = app.config.get("CAPTCHA_SECRET")
        payload = {'response':data["g-recaptcha-response"], 'secret':secret}
        response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
        response_text = json.loads(response.text)
        if not response_text['success']:
            raise SystemException("Invalid captcha, please try again", SystemException.FIELD_ERROR)
        return f(**kws)
    return ValidateFields