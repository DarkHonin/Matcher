from pymongo.collection import Collection
from systems.exceptions import UserCreateException
import copy
import json
from datetime import datetime
import sys
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
import re

class DBDocument:

    collection_name = None

    def __init__(self, _id : ObjectId=None):
        if _id:
            self._id = _id

    def getFields(self):
        return []

    def getCollectionName(self):
        return ""

    @classmethod
    def collection(clls):
        from app import Database
        if clls.collection_name not in Database.db.collection_names():
            print("Loading database keys")
            col = Database.db[clls.collection_name]
            clls.defineKeys(col)
        else:
            col = Database.db[clls.collection_name]
        return col

    #Helper functions

    @staticmethod
    def encodeDBDocumentElement(data):
        ret = {}
        if isinstance(data, DBDocument):
            return data.encodeDocument()
        if isinstance(data, list):
            ret = []
            for e in data:
                ret.append(DBDocument.encodeDBDocumentElement(e))
            return ret
        if isinstance(data, dict):
            for k, v in data.items():
                ret[k] = DBDocument.encodeDBDocumentElement(v)
            return ret
        return data

    def encodeDocument(self):
        ret = {"class" : str(self.__class__)}
        for k, v in self.__dict__.items():
            ret[k] = DBDocument.encodeDBDocumentElement(v)
        return ret

    @staticmethod
    def getClassFromString(st):
        m = re.search("'(.+?)'", st)
        if not m:
            return None
        classParts = m.group(1).split(".")        
        clsname = classParts.pop()
        namespace = ".".join(classParts)
        return getattr(sys.modules[namespace], clsname)

    @staticmethod
    def decodeDocument(dt):
        if not isinstance(dt, dict) or "class" not in dt:
            return dt
        cl = DBDocument.getClassFromString(dt.pop("class"))
        instance = cl.__new__(cl)
        for k, v in dt.items():
            if isinstance(v, dict):
                if "class" in v:
                    setattr(instance, k, DBDocument.decodeDocument(v))
            elif isinstance(v, list):
                setattr(instance, k, [])
                for s in v:
                    getattr(instance, k).append(DBDocument.decodeDocument(s))
            else:
                setattr(instance, k, v)
        return instance

    def toJSON(self):
        data = self.__dict__
        data["__class"] = str(self.__class__)
        return data

    @staticmethod
    def fromJSON(json):
        cl = DBDocument.getClassFromString(json.pop("__class"))
        instance = cl.__new__()
        for e, v in json.items():
            if isinstance(v, dict) and "__class" in v:
                setattr(instance, e, DBDocument.fromJSON(json[e]))
            elif e == "_id":
                setattr(instance, e, ObjectId(json[e]))    
            else:
                setattr(instance, e, json[e])
        return instance

    @classmethod
    def defineKeys(clls, collection):
        pass

    #end Helper functions


    @classmethod
    def get(clss, where={}, what : dict = None):
        from app import Database
        hip = clss.collection_name
        col = Database.db[hip]
        items = col.find(where, what)
        ret = []
        for item in items:
            inst = clss.decodeDocument(item)
            ret.append(inst)
        if len(ret) == 1:
            return ret.pop()
        elif len(ret) == 0:
            return False
        return ret

    def save(self):
        try:
            self.lastChanged = datetime.now()
            if  not "_id" in self.__dict__:
                if self.collection() == 0:
                    self.defineKeys(self.collection())
                id = self.collection().insert_one(self.encodeDocument())
                self._id = id.inserted_id
                print("%s inserted at %s" % (self.__class__.__name__, str(self._id)))
            else:
                self.collection().update_one({"_id" : self._id}, {"$set" : self.encodeDocument()})
                print("%s updated %s" % (self.__class__.__name__, str(self._id)))
        except DuplicateKeyError:
            raise UserCreateException("Username/Email already in use.")

    def delete(self):
        self.collection().delete_one({"_id" : self._id})

    def toDisplaySet(self):
        item = copy.deepcopy(self)
        del(item._id)
        return item.__dict__