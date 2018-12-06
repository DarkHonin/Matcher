from systems.database import DBDocument
from systems.users.user import User
from datetime import datetime, timedelta
import flask

class Telemetry(DBDocument):

    collection_name = "Telemetry"

    def __init__(self):
        self._viewers = []  # The users who have viewed this page
        self._viewed = []   # The pages the user has viewed
        self._likes = []    # The pages the user has blocked
        self._blocked = []
        self.created = datetime.now()
        self.lastView = datetime.now()
        pass

    def wasViewedBy(self, user : User):
        if user._id not in self._viewers:
            self._viewers.append(user._id)

    def isViewing(self, user : User):
        if user._id not in self._viewed:
            self._viewed.append(user._id)

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
        return self.notifications

    def postMessage(self, string, actingID):
        if "_blocked" not in self.__dict__:
            self._blocked = []
        if "notifications" not in self.__dict__:
            self.notifications = []
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
            if subject._id in actor.telemetry._likes and actor._id in subject.telemetry._likes:
                from systems.users import Chat
                Chat.spawnChat(subject, actor)
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