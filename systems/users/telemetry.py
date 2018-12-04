from systems.database import DBDocument
from systems.users.user import User
from datetime import datetime

class Telemetry(DBDocument):
    def __init__(self):
        self.viewdBy = []
        self.viewed = []
        self.liked = []
        self.notifications = []
        self.created = datetime.now()
        self.lastView = datetime.now()
        pass

    def likes(self):
        ret = User.get({"_id": {"$in": self.liked}}, {"uname" : 1, "info.images" : 1, "last_online" : 1})
        if isinstance(ret, list):
            return ret
        return [ret]

    def viewHistory(self):
        ret = User.get({"_id": {"$in": self.viewed}}, {"uname" : 1, "info.images" : 1, "last_online" : 1})
        if isinstance(ret, list):
            return ret
        return [ret]

    def viewers(self):
        ret = User.get({"_id": {"$in": self.viewdBy}}, {"uname" : 1, "info.images" : 1, "last_online" : 1})
        if isinstance(ret, list):
            return ret
        return [ret]

    def viewing(self, user):
        if "viewed" not in self.__dict__:
           self.viewed = [] 
        if(user._id not in self.viewed):
            self.viewed.append(user._id)

    def view(self, user):
        if(user._id in self.viewdBy):
            return 
        self.viewdBy.append(user._id)
        self.notifications.append({ "time" : datetime.now(), "message" : "%s just viewed your profile" % user.uname, "read" : False , "displayed" : False})

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