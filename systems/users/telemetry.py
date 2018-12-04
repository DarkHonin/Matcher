from systems.database import DBDocument
from systems.users.user import User
from datetime import datetime

class Telemetry(DBDocument):
    def __init__(self):
        self.viewdBy = []
        self.liked = []
        self.created = datetime.now()
        self.lastView = datetime.now()
        pass

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
        base = datetime.now() - self.created
        sinceLastEdit = datetime.now() - self.lastView
        delta = base - sinceLastEdit
        print("time since last edit: %s" % delta)
        prs = delta / base
        print("Modifyer: %s" % prs)
        ret = len(self.viewdBy) * prs
        return int(ret)

    def handle(self, field, value):
        if field == "genderInterest":
            self.genderInterest = ["Men", "Both", "Women"].index(value)

    def getCollectionName(self):
        return "Telemetry"