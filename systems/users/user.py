from systems.database import DBDocument
from systems.exceptions import SystemException
from systems.properties import USERNAME, EMAIL, PASSWORD
from flask import session
import datetime
class User(DBDocument):

    collection_name =  "Users"

    def __init__(self, uname, email):
        DBDocument.__init__(self)
        self.uname = uname
        self._email = email
        self.active = False
        self.email_valid = False
        self.hash = None
        self.last_online = datetime.datetime.now()
        self.info = None
        self.telemetry = None

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
        self.save()
        return True

    def logout(self):
        from views.SocketSystems import SocketSystem
        if session["user"] in SocketSystem.CONNECTED_USERS:
            del(SocketSystem.CONNECTED_USERS[session["user"]])
        del(session["user"])

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

    @classmethod
    def parent(cls, instance):
        return super(cls, instance)