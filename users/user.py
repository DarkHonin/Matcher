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
            tt = Token(user, "activate")
            sendTokenEmail(email, tt)
        except InvalidEmailMessage as e:
            user.delete()
            raise e

####################################################################################################################################################################################

    def __init__(self, uname, email, password):
        self.email = email
        self.password = password
        self.uname = uname
        self.loginToken = None
        self.active = False

    @property
    def password(self):
        return None

    @password.setter
    def password(self, password):
        self.hash = generate_password_hash(password)

    def login(self, password):
        if not (check_password_hash(self.hash, password)):
            return False
        self.loginToken = str(uuid4())
        del(self.hash)
        self.save()
        session["user"] = self
        return True

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

    def save(self):
        super().save()
        if "user" in session:
            session["user"] = self

    @staticmethod
    def defineKeys(col):
        col.create_index(("uname"), unique=True)
        col.create_index(("_email"), unique=True)

    def DuplicateKeyError(self):
        raise APIException(message="Username/Email aready in use")
