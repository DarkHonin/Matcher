from app import DATABASE
from pymongo.collection import Collection
import copy
import json
from datetime import datetime
import sys
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
import re
from app.api import APIException

class DBDocument:

    collection_name = None

    def __init__(self, _id : ObjectId=None):
        if _id:
            self._id = _id

    @classmethod
    def collection(clls):
        if not DATABASE.db:
            raise APIException(message="Database not available")
        col = DATABASE.db[clls.collection_name]
        if clls.collection_name not in DATABASE.db.collection_names():
            print("Loading database keys")
            clls.defineKeys(col)
        return col

    #Helper functions

    @staticmethod
    def encodeDBDocumentElement(data):
        ret = {}
        if isinstance(data, DBDocument):
            return data.encodeDocument()
        if isinstance(data, list):
            if not data:
                return []
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
        try:
            ret = {"class" : str(self.__class__)}
            for k, v in self.__dict__.items():
                if v is not self:
                    ret[k] = DBDocument.encodeDBDocumentElement(v)
        except RecursionError:
            print(ret)
            raise Exception(str(ret))
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
                else:
                    setattr(instance, k, v)
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

    def sync(self):
        data = self.get({"_id" : self._id})
        self.__dict__ = data.__dict__

    @staticmethod
    def fromJSON(json):
        cl = DBDocument.getClassFromString(json.pop("__class"))
        instance = cl.__new__(cl)
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
    def get(clss, where : dict={}, what : dict = None):
        print("Document GET :: ", clss)
        from app import DATABASE
        hip = clss.collection_name
        col = DATABASE.db[hip]
        if("_id" in where):
            if not isinstance(where["_id"], ObjectId) and isinstance(where["_id"], str):
                where["_id"] = ObjectId(where["_id"])
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
            if hasattr(self, "_id"):
                self.collection().update_one({"_id" : self._id}, {"$set" : self.encodeDocument()})
            else:
                if self.collection() == 0:
                    self.defineKeys(self.collection())
                qq = self.collection().insert_one(self.encodeDocument())
                self._id = qq.inserted_id
        except DuplicateKeyError as e:
            if hasattr(self, "DuplicateKeyError"):
                getattr(self, "DuplicateKeyError")()
            else:
                raise e

    def delete(self):
        print(self.collection().delete_one({"_id" : self._id}))

    def toDisplaySet(self):
        item = copy.deepcopy(self)
        del(item._id)
        return item.__dict__