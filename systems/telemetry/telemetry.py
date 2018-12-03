from systems.database import DBDocument
from systems.users.user import User
from datetime import datetime

class Telemetry(DBDocument):
    def __init__(self,user:User, genderInterest, location):
        DBDocument.__init__(self)
        self._user = user
        self.pageViews=[]
        self.genderInterest=str(genderInterest)
        self.location = location
        self.likes = []
        self.blocked = []
        self.reportedBy = []

    @staticmethod
    def forUser(user : User):
        return Telemetry.get({"user" : str(user._id)})

    @property
    def user(self):
        return str(self._user._id)

    @user.setter
    def user(self, id:str):
        self._user = User.get({"_id" : id}, {"hash" : 0})

    def fame(self):
        #print("%s - %s = %s" % (self.lastChanged, datetime.now(), datetime.now() - self.lastChanged))
        base = datetime.now() - self.created
        sinceLastEdit = datetime.now() - self.lastChanged
        delta = base - sinceLastEdit
        print("time since last edit: %s" % delta)
        prs = delta / base
        print("Modifyer: %s" % prs)
        ret = len(self.pageViews) * prs
        return int(ret)

    def handle(self, field, value):
        if field == "genderInterest":
            self.genderInterest = ["Men", "Both", "Women"].index(value)

    def getFields(self):
        return ["user", "pageViews", "genderInterest", "location"]

    def getCollectionName(self):
        return "Telemetry"