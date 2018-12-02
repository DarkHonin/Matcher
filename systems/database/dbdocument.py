from pymongo.collection import Collection
from systems.exceptions import UserCreateException
import copy
import json
from datetime import datetime
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId


class DBDocument:
    def __init__(self):
        self._id = False
        self.lastChanged = None
        self.created = datetime.now()

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
        for i in self.getFields() + ["lastChanged", "created", "_id"]:
            if hasattr(self, i):
                attr = self.__getattribute__(i)
                if(i == "_id"):
                    yield i, str(attr)
                else:
                    yield i, attr

    def set_values(self, data):
        for k, v in data.items():
            setattr(self, k, v)

    def defineKeys(self, collection):
        pass

    #end Helper functions

    @classmethod
    def get(class_object, where={}, what : dict = None, sort=None):
        if "_id" in where:
            if type(where['_id']) is str:
                where["_id"] = ObjectId(where["_id"])
        instance = class_object.__new__(class_object)
        if sort:
            items = instance.collection.find(where, what).sort(sort)
        else:    
            items = instance.collection.find(where, what)
        ret = []
        for item in items:
            subi = copy.deepcopy(instance)
            subi.set_values(item)
            ret.append(subi)
        if len(ret) == 1:
            return ret.pop()
        elif len(ret) == 0:
            return False
        return ret

    def save(self):
        try:
            self.lastChanged = datetime.now()
            data = dict(self)
            del(data['_id'])
            if not self._id:
                id = self.collection.insert_one(data)
                self._id = str(id.inserted_id)
                print("%s inserted at %s" % (self.__class__.__name__, str(self._id)))
            else:
                id = ObjectId(str(self._id))
                self.collection.update_one({"_id" : id}, {"$set" : data})
                print("%s updated %s" % (self.__class__.__name__, str(self._id)))
        except DuplicateKeyError:
            raise UserCreateException("Username/Email already in use.")

    def delete(self):
        self.collection.delete_one({"_id" : self._id})

    def toDisplaySet(self):
        item = copy.deepcopy(self)
        del(item._id)
        return item.__dict__