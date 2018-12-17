from database import DBDocument
from .profile import Profile
from uuid import uuid4
from api import APIException
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from .tokens import sendTokenEmail, Token, InvalidEmailMessage

class User(DBDocument):

    collection_name = "Users"

    @staticmethod
    def registerNewUser(uname, email,password, **kwargs):
        from .page import Page
        from app import APP
        user = User(uname, email, password)
        kwargs.pop("g-recaptcha-response")
        user.save()
        det = Profile(user=user, **kwargs)
        det.save()
        if not APP.config["ALWAYS_ACTIVE"]:
            try:
                tt = Token(user, "validate_email")
                sendTokenEmail(email, tt)
            except InvalidEmailMessage as e:
                user.delete()
                det.delete()
                raise e

####################################################################################################################################################################################

    def __init__(self, uname, email, password):
        from app import APP
        self.email = email
        self.set_password(password)
        self.uname = uname
        self.email_valid = False
        self.active = APP.config["ALWAYS_ACTIVE"]
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
        session["user"] = self._id
        return True

    @property
    def location(self):
        print("geting location")
        from flask import request
        import requests
        url = "http://api.ipstack.com/%s?access_key=c3d5cfa1b31c8989bb9c1d4f36cc096b" % request.environ['REMOTE_ADDR']
        response = requests.get(url).json()
        print("Location discovered")
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
        col.create_index(("email"), unique=True)

    def DuplicateKeyError(self):
        raise APIException(message="Username/Email aready in use")

    def isOnline(self):
        from messageing.Sockets import MessageSockets
        return self.uname in MessageSockets.INSTANCE.rooms