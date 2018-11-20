from . import DataObject

class User(DataObject):
    def __init__(self):
        DataObject.__init__(self, 
            {
                "uname"         : None,
                "email"         : None,
                "email_valid"   : False,
                "lname"         : None,
                "fname"         : None,
                "active"        : False
            }, "Users"
        )

    def isValid(self):
        unames = self.getAll(User, {"uname" : self.uname['value']})
        if(unames):
            print("Uname is not ok")
            return {"status":"NOJOY", "message":"Username in use"}
        print("Uname is ok")

        return False
        