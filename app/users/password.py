from app.obj import DataObject
from app.token import Token

class Password(DataObject):

    def __init__(self, hash=None, user=None):
        DataObject.__init__(self,  "Passwords")
        self.user = user
        self.hash = hash

    def fieldKeys(self):
        return ["user", "hash"]

    def key_error(self):
        return "Username/Email already in use"

    def init_index(self, col):
        col.create_index(("user"), unique=True)