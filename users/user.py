from database import DBDocument
from .user_info import UserInfo
from uuid import uuid4
from api import APIException
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from .tokens import sendTokenEmail, Token, InvalidEmailMessage

class User(DBDocument):

    collection_name = "Users"

    @staticmethod
    def registerNewUser(uname, email,password, **kwargs):
        user = User(uname, email, password)
        kwargs.pop("g-recaptcha-response")
        det = UserInfo(**kwargs)
        det.save()
        user.details = det._id
        user.save()		
        try:
            tt = Token(user, "validate_email")
            sendTokenEmail(email, tt)
        except InvalidEmailMessage as e:
            user.delete()
            raise e

####################################################################################################################################################################################

    def __init__(self, uname, email, password):
        self.email = email
        self.password = password
        self.uname = uname
        self.email_valid = False
        self.loginToken = None
        self.active = False
        self.details = None

    def set_password(self, password):
        self.hash = generate_password_hash(password)
        return ""

    def set_email(self, email):
        if email == self.email:
            return
        self.email_valid = False
        self.email = email
        if self._id:
            from .tokens import Token, sendTokenEmail
            token = Token(self, "validate_email")
            token.save()
            sendTokenEmail(self.email, token)
        return email

    def set_uname(self, value):
        self.uname = value
        return value
    
    def login(self, password):
        if not (check_password_hash(self.hash, password)):
            return False
        self.loginToken = str(uuid4())
        self.save()
        info = UserInfo.get({"_id" : self.details})
        info.location = self.location
        session["user"] = self._id
        return True

    @property
    def location(self):
        from flask import request
        import requests
        url = "http://api.ipstack.com/%s?access_key=c3d5cfa1b31c8989bb9c1d4f36cc096b" % request.environ['REMOTE_ADDR']
        response = requests.get(url).json()
        if not self.location:
            if(not response['latitude']):
                return [0, 0]
            else:
                return [response['latitude'], response["longitude"]]

    def activate(self):
        self.active = True
        self.save()

    def verify(self):
        i = self.get({"loginToken" : self.loginToken}, {"_id" : 1})
        if not i:
            return False
        self.loginToken = str(uuid4())
        self.save()
        return True


    def validate_email(self):
        self.email_valid = True
        self.active = True
        self.save()


    @staticmethod
    def defineKeys(col):
        col.create_index(("uname"), unique=True)
        col.create_index(("_email"), unique=True)

    def DuplicateKeyError(self):
        raise APIException(message="Username/Email aready in use")
