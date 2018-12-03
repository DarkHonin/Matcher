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

    def set_values(self, data):
        for k, v in data.items():
            print("setting %s %s in %s" % (k, v, __class__))
            setattr(self, k, v)

    def encodeDocument(self):
        ret = {}
        for k, v in self.__dict__.items():
            if isinstance(v, DBDocument):
                if("classes" not in ret):
                    ret.update({"classes" : {}})
                ret["classes"][k] = str(v.__class__)
                ret[k] = v.encodeDocument()
            else:
                ret[k] = v
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

    @classmethod
    def decodeDocument(lc, dt:dict):
        classes = {}
        instance = lc.__new__(lc)
        if "classes" in dt:
            classes = dt.pop("classes")
        for k, v in dt.items():
            if k in classes and isinstance(v, dict):
                cl = DBDocument.getClassFromString(classes[k])
                setattr(instance, k, cl.decodeDocument(v))
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