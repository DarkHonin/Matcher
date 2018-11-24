from app.obj import DataObject
from app.token import Token
from app.validator import Validator, EMAIL_FIELD, UNAME_FIELD, Field
import uuid

class User(DataObject):

   

    GENDER = {
        "Male" : 0,
        "Female" : 1
    }

    SEXUALITY = {
        "Men"               : 0,
        "Women"             : 1,
        "Both"              : 2,
        "Prefer not to say" : 3
    }

    PUBLIC_FIELDS = [
	    UNAME_FIELD,
        Field("fname", {"Not a valid first name" : Validator.isValidName}, True, "First name"),
        Field("lname", {"Not a valid first name" : Validator.isValidName}, True, "Last name"),
        Field("gender", Validator.oneOf, False, "Gender", "enum", GENDER),
        Field("Sexuality", Validator.oneOf, False, "Interested in", "enum", SEXUALITY),
    ]

    PRIVATE_FIELDS = [
        EMAIL_FIELD
    ]

    def __init__(self):
        DataObject.__init__(self, "Users")
        self.uname         = None
        self.email         = None
        self.email_valid   = False
        self.lname         = None
        self.fname         = None
        self.active        = False
        self.gender        = None
        self.Sexuality     = None
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
            "Sexuality",
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