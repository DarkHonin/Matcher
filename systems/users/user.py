from systems.database import DBDocument
from systems.exceptions import SystemException
from flask import session
class User(DBDocument):

    def __init__(self, uname, email, password):
        DBDocument.__init__(self)
        self.uname = uname
        self.hash = None
        self.password = password
        self._email = email
        self.email_valid = False

    def activate(self):
        self.email_valid = True
        self.save()

    def login(self, password):
        from werkzeug.security import check_password_hash
        if not (check_password_hash(self.hash, password)):
            raise SystemException("Username/Password invalid", SystemException.USER_CREATE_EXCEPTION)
        session_info = dict(self)
        del(session_info['hash'])
        session["user"] = session_info
        return True

    def logout(self):
        del(session["user"])

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
        self.email_valid = False
        self._email = email
        pass

    def defineKeys(self, col):
        col.create_index(("uname"), unique=True)
        col.create_index(("_email"), unique=True)

    def getFields(self):
        return ["uname", "hash", "_email", "email_valid"]

    def getCollectionName(self):
        return "Users"

    def save(self):
        from systems.tokens import Token
        super().save()
        token = Token(self, "activate")
        token.save()