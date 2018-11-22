from app.obj import DataObject
from flask_pymongo import PyMongo
from app.token import Token

class User(DataObject):

    GENDER = {
        "Male" : 0,
        "Female" : 1
    }

    SEXUALITY = {
        "Straight"          : 0,
        "Bisexual"          : 1,
        "Homosexual"        : 2,
        "Prefer not to say" : 1
    }

    def __init__(self):
        DataObject.__init__(self, 
            {
                "uname"         : None,
                "email"         : None,
                "email_valid"   : False,
                "lname"         : None,
                "fname"         : None,
                "password"      : None,
                "active"        : False,
                "gender"        : -1,
                "Sexuality"     : -1,
                "Biography"     : None,
                "Images"        : [],
                "Location"      : None,
                "lastLogin"     : None,
                "sessionID"     : None
            }, "Users"
        )

    def key_error(self):
        return "Username/Email already in use"

    def init_index(self, col):
        col.create_index(("uname"), unique=True)
        col.create_index(("email"), unique=True)
        
    def activate(self, t : Token):
        print("Activating user: %s" % self.uname['value'])
        self.active['value'] = True
        self.email_valid['value'] = True
        self.save()
        pass