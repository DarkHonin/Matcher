from systems.database import DBDocument
from systems.exceptions import SystemException
from systems.properties import USERNAME, EMAIL, PASSWORD
from flask import session
class User(DBDocument):

    def __init__(self, uname, email, password):
        DBDocument.__init__(self)
        self.uname = uname
        self.hash = None
        self.password = password
        self._email = email
        self.active = False
        self.email_valid = False

    def validate_email(self):
        self.email_valid = True
        self.save()

    def login(self, password):
        from werkzeug.security import check_password_hash
        if not (check_password_hash(self.hash, password)):
            raise SystemException("Username/Password invalid", SystemException.USER_CREATE_EXCEPTION)
        session["user"] = str(self._id)
        return True

    def logout(self):
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

    def defineKeys(self, col):
        col.create_index(("uname"), unique=True)
        col.create_index(("_email"), unique=True)

    def getFields(self):
        return ["uname", "hash", "_email", "email_valid", "active"]

    def getCollectionName(self):
        return "Users"

    def register(self):
        self.save()
        from systems.tokens import Token, sendTokenEmail
        token = Token(self, "validate_email")
        token.save()
        sendTokenEmail(self.email, token)

    @classmethod
    def parent(cls, instance):
        return super(cls, instance)