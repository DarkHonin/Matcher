from systems.database import DBDocument
from systems.users.user import User
from datetime import datetime, timedelta

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