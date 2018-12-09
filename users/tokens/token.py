from database import DBDocument
import uuid
import datetime
class Token(DBDocument):

    collection_name = "Tokens"

    def __init__(self, subject : DBDocument, action):
        DBDocument.__init__(self)
        self.subject = subject
        from app import APP
        if(APP.config["TESTING_APP"]):
            self.token = APP.config["TESTING_TOKEN"]
        else:
            self.token = uuid.uuid4()
        self.time = datetime.datetime.now()
        self.action = action

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, subject : DBDocument):
        self._subject = {"class" : str(subject.__class__), "_id" : subject._id}