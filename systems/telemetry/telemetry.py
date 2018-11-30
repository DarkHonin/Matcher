from systems.database import DBDocument
from systems.users.user import User
from datetime import datetime

class Telemetry(DBDocument):
    def __init__(self,user:User, genderInterest, location):
        DBDocument.__init__(self)
        self._user = user
        self.pageViews="0"
        self.genderInterest=str(genderInterest)
        self.location = location

    @staticmethod
    def forUser(user : User):
        return Telemetry.get({"user" : user._id})

    @property
    def user(self):
        return str(self._user._id)

    @user.setter
    def user(self, id:str):
        self._user = User.get({"_id" : id}, {"hash" : 0})

    @property
    def fame(self):
        delta = self.lastChanged - datetime.now()
        prs = delta / datetime.now().total_seconds()
        return self.pageViews * prs

    def handle(self, field, value):
        if field == "genderInterest":
            self.genderInterest = ["Men", "Both", "Women"].index(value)

    def getFields(self):
        return ["user", "pageViews", "genderInterest", "location"]

    def getCollectionName(self):
        return "Telemetry"