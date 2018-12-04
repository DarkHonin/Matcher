from systems.database import DBDocument
from systems.exceptions import SystemException
from systems.properties import USERNAME, EMAIL, PASSWORD
from flask import session
import datetime
from uuid import uuid3, NAMESPACE_URL
class User(DBDocument):

    collection_name =  "Users"

    def __init__(self, uname, email):
        DBDocument.__init__(self)
        self.uname = uname
        self._email = email
        self.active = False
        self.email_valid = False
        self.hash = None
        self.last_online = None
        self.info = None
        self.telemetry = None
        self.token = None

    def validate_email(self):
        self.email_valid = True
        self.save()

    def activate(self):
        if self.info.complete:
            from systems.users import Telemetry
            self.active = True
            self.telemetry = Telemetry()
        self.save()

    def login(self, password):
        from werkzeug.security import check_password_hash
        if not (check_password_hash(self.hash, password)):
            raise SystemException("Username/Password invalid", SystemException.USER_CREATE_EXCEPTION)
        session["user"] = self._id
        self.last_login = datetime.datetime.now()
        self.last_online = self.last_login
        self.token = uuid3(NAMESPACE_URL, self.uname)
        self.save()
        return True

    def logout(self):
        self.token = None
        del(session["user"])
        self.save()

    def toJSON(self):
        hold = super().toJSON()
        hold["online"] = self.online()
        return hold

    @property
    def fields(self):
        return [USERNAME, EMAIL, PASSWORD]

    @property
    def password(self):
        pass
    
    @password.setter
    def password(self, password):
        from werkzeug.security import generate_password_hash
        self.hash = generate_password_hash(password)

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email):
        if email == self._email:
            return
        self.email_valid = False
        self._email = email
        if self._id:
            from systems.tokens import Token, sendTokenEmail
            token = Token(self, "activate")
            token.save()
            sendTokenEmail(self.email, token)
        pass

    @staticmethod
    def defineKeys(col):
        col.create_index(("uname"), unique=True)
        col.create_index(("_email"), unique=True)

    def register(self):
        self.save()
        from systems.tokens import Token, sendTokenEmail
        token = Token(self, "validate_email")
        try:
            sendTokenEmail(self.email, token)
            token.save()
        except SystemException as e:
            self.delete()
            raise e

    def online(self):
        if not self.last_online:
            return -1
        delta = datetime.datetime.now() - self.last_online
        if delta > datetime.timedelta(minutes=15):
            return 0
        if delta > datetime.timedelta(minutes=30):
            return -1
        return 1
