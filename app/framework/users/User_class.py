import flask
from app.framework import DataObject, Token
from app.framework.validator import *
import uuid

class User(DataObject):

    GENDER = [
            "Male",
            "Female"
        ]

    SEXUALITY = [
        "Men"               ,
        "Women"             ,
        "Both"              ,
        "Prefer not to say" 
    ]
    
    PUBLIC_FIELDS = [
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
        self._gender        = None
        self._sexuality     = None
        self.Biography     = None
        self.Images        = []
        self.Location      = None
        self.lastLogin       = None
        self.sessionID     = None
        self.uid = uuid.uuid1().hex
       
    def fieldKeys(self):
        return [
            "uid",
            "uname",
            "email",
            "email_valid",
            "lname",
            "fname",
            "active",
            "gender",
            "sexuality",
            "Biography",
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