from systems.users import User, UserInfo
from systems.database import DBDocument
import uuid
import datetime
class Token(DBDocument):
    def __init__(self, subject : DBDocument, action):
        DBDocument.__init__(self)
        self.subject = subject
        from app import app
        if(app.config["TESTING_APP"]):
            self.token = app.config["TESTING_TOKEN"]
        else:
            self.token = uuid.uuid4()
        self.time = datetime.datetime.now()
        self.action = action

    def getFields(self):
        return ["_subject", "token", "action"]

    def getCollectionName(self):
        return "Tokens"

    @property
    def subject(self):
        import sys
        from bson.objectid import ObjectId
        classname = getattr(sys.modules[__name__], self._subject['class'])
        return classname.get({"_id" :ObjectId( str(self._subject['_id']))})

    @subject.setter
    def subject(self, subject : DBDocument):
        self._subject = {"class" : subject.__class__.__name__, "_id" : subject._id}