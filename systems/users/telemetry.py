from systems.database import DBDocument
from systems.users.user import User
from datetime import datetime, timedelta
import flask

class Notification(DBDocument):
    def __init__(self, message, actor):
        DBDocument.__init__(self)
        self.created = datetime.now()
        self.message = message
        self.read = False
        self.displayed = False
        self.actor = actor

    @property
    def display(self):
        self.displayed = True
        return self.message

    @property
    def age(self):
        delta = datetime.now() - self.created
        delta = delta.total_seconds()
        for k, v in {"sec" : 60, "min" : 60, "hour/s" : 60, "days" : 2}.items():
            if delta < v:
                return "%s %s" % (int(delta), k)
            else:
                delta = delta / v
        return self.created.strftime("dd-MM-YYYY")

    @property
    def actingUser(self):
        if "actor" not in self.__dict__:
            return "#"
        user = User.get({"_id" : self.actor}, {"class" : 1, "uname" : 1})
        return flask.url_for("user", name=user.uname)

    @property
    def readit(self):
        holder = self.read
        self.read = True
        return holder

class Telemetry(DBDocument):
    def __init__(self):
        self._viewers = []  # The users who have viewed this page
        self._viewed = []   # The pages the user has viewed
        self._likes = []    # The pages the user has blocked
        self._blocked = []
        self.notifications = []
        self.created = datetime.now()
        self.lastView = datetime.now()
        pass

    def getLikes(self):
        ret = User.get({"_id": {"$in": self._likes}}, {"uname" : 1, "info.images" : 1, "last_online" : 1})
        if isinstance(ret, list):
            return ret
        return [ret]

    def likes(self, user):
        return user._id in self._likes

    def viewHistory(self):
        ret = User.get({"_id": {"$in": self._viewed}}, {"uname" : 1, "info.images" : 1, "last_online" : 1})
        if isinstance(ret, list):
            return ret
        return [ret]

    def viewers(self):
        ret = User.get({"_id": {"$in": self._viewers}}, {"uname" : 1, "info.images" : 1, "last_online" : 1})
        if isinstance(ret, list):
            return ret
        return [ret]

    @property
    def alerts(self):
        self.notifications.sort(key=lambda x : x.created, reverse=True)
        return self.notifications[:10]

    def postMessage(self, string, actingID):
        if "_blocked" not in self.__dict__:
            self._blocked = []
        if actingID not in self._blocked:
            self.notifications.append(
                Notification(string, actingID)
            )

    @staticmethod
    def view(user_page : User, user : User):
        if user._id not in user_page.telemetry._viewers:
            user_page.telemetry.postMessage("%s just viewed your profile" % user.uname, user._id)
            user_page.telemetry._viewers.append(user._id)
            user_page.save()
        if user_page._id not in user.telemetry._viewed:
            user.telemetry._viewed.append(user_page._id)
            user.save()
        

        
    @staticmethod
    def like(actor : User, subject : User):
        if subject._id not in actor.telemetry._likes:
            actor.telemetry._likes.append(subject._id)
            subject.telemetry.postMessage("%s just liked your profile" % actor.uname, actor._id)
            actor.save()
            subject.save()
            return True
        actor.telemetry._likes.remove(subject._id)
        subject.telemetry.postMessage("%s just displiked your profile" % actor.uname, actor._id)
        actor.save()
        subject.save()
        return False

    def block(self, badguy):
        if badguy._id not in self._blocked:
            self._blocked.append(badguy._id)

    def fame(self):
        base = datetime.now() - self.created
        sinceLastEdit = datetime.now() - self.lastView
        delta = base - sinceLastEdit
        print("time since last edit: %s" % delta)
        prs = delta / base
        print("Modifyer: %s" % prs)
        ret = len(self._viewers) * prs
        return int(ret)

    def handle(self, field, value):
        if field == "genderInterest":
            self.genderInterest = ["Men", "Both", "Women"].index(value)

    def getCollectionName(self):
        return "Telemetry"