from pymongo.collection import Collection
from systems.exceptions import UserCreateException
import copy
from datetime import datetime
from pymongo.errors import DuplicateKeyError

class DBDocument:
    def __init__(self):
        self._id = False
        self.lastChanged = None

    def getFields(self):
        return []

    def getCollectionName(self):
        return ""

    @property
    def collection(self):
        from app import Database
        if self.getCollectionName() not in Database.db.collection_names():
            print("Loading database keys")
            col = Database.db[self.getCollectionName()]
            self.defineKeys(col)
        else:
            col = Database.db[self.getCollectionName()]
        return col

    #Helper functions

    def __iter__(self):
        for i in self.getFields() + ["lastChanged"]:
            yield i, self.__getattribute__(i)

    def defineKeys(self, collection):
        pass

    #end Helper functions

    @classmethod
    def get(class_object, where={}, what : dict = None):
        instance = class_object.__new__(class_object)
        items = instance.collection.find(where, what)
        ret = []
        for item in items:
            subi = copy.deepcopy(instance)
            for k, v in item.items():
                setattr(subi, k, v)
            ret.append(subi)
        if len(ret) == 1:
            return ret.pop()
        elif len(ret) == 0:
            return False
        return ret

    def save(self):
        try:
            self.lastChanged = datetime.now()
            if not self._id:
                id = self.collection.insert_one(dict(self))
                self._id = id.inserted_id
                print("%s inserted at %s" % (self.__class__.__name__, str(self._id)))
            else:
                self.collection.update_one({"_id" : self._id}, {"$set" : dict(self)})
                print("%s updated %s" % (self.__class__.__name__, str(self._id)))
        except DuplicateKeyError:
            raise UserCreateException("Username/Email already in use.")

    def delete(self):
        self.collection.delete_one({"_id" : self._id})