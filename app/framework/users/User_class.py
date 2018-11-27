import flask
from app.framework import DataObject, Token
from app.framework.validator import *
import uuid

class User(DataObject):

    GENDER = [
            "Prefer not to say",
            "Male",
            "Female"
        ]

    SEXUALITY = [
        "Prefer not to say" ,
        "Men"               ,
        "Women"             ,
        "Both"              ,
    ]
    
    PUBLIC_FIELDS = [
        Field("biography", {}, False, "Biography", "blob"),
	    UNAME_FIELD,
        Field("fname", {"Not a valid first name" : Validator.isValidName}, True, "First name"),
        Field("lname", {"Not a valid first name" : Validator.isValidName}, True, "Last name"),
        Field("gender", {"Not a valid gender":Validator.oneOf}, False, "Gender", "enum", GENDER),
        Field("sexuality", {"Its cool that your into that but we cant show that here":Validator.oneOf}, False, "Interested in", "enum", SEXUALITY),
    ]

    PRIVATE_FIELDS = [
        EMAIL_FIELD,
        PASSWORD_FIELD
    ]

    FIELDS = PUBLIC_FIELDS + PRIVATE_FIELDS

    GLOBAL_VALIDATOR = Validator(FIELDS)

    def __init__(self):
        DataObject.__init__(self, "Users")
        self.uname         = None
        self.email         = None
        self.email_valid   = False
        self.lname         = None
        self.fname         = None
        self.active        = False
        self._gender        = "Prefer not to say"
        self._sexuality     = "Prefer not to say"
        self.biography     = None
        self.images        = []
        self.Location      = None
        self.lastLogin       = None
        self.sessionID     = None
        self.uid = uuid.uuid1().hex
       
    def fieldKeys(self):
        return [
            "uid",
            "uname",
            "lname",
            "fname",
            "email",
            "biography",
            "email_valid",
            "active",
            "gender",
            "sexuality",
            "Location",
            "lastLogin"
        ]

    def key_error(self):
        return "Username/Email already in use"

    def init_index(self, col):
        col.create_index(("uname"), unique=True)
        col.create_index(("email"), unique=True)
        
    def activate(self, t : Token):
        print("Activating user: %s" % self.uname)
        self.active = True
        self.email_valid = True
        pass

    def isComplete(self):
        for i in self.fieldKeys():
            if(not self.__getattribute__(i)):
                return False
        return True

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value:str):
        if value not in self.GENDER:
            raise Exception("User gender must be one of %s" % self.GENDER)
        self._gender = value

    @property
    def sexuality(self):
        return self._sexuality

    @sexuality.setter
    def sexuality(self, value:str):
        if value not in self.SEXUALITY:
            raise Exception("User gender must be one of %s" % self.SEXUALITY)
        self._sexuality = value

    @property
    def password(self):
        return "Your super secret password"

    @password.setter
    def password(self, password):
        if not self.id:
            raise Exception("User cannot have password if not saved")
        from app.framework.users.password import Password
        from werkzeug.security import generate_password_hash
        pwd = Password.get(Password, {"user" : self.id})
        if( not pwd):
            pwd = Password(generate_password_hash(password), self.id)
        pwd.save()

    def hasMaxImages(self):
        return len(self.images) < 5