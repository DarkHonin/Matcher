
class DataObject:
    def __init__(self, collection : str):
        self.collection = collection
        self.id = -1
        self.ERROR = False

    def fieldKeys(self):
        return []

    def log_fields(self):
        print("-"*((15*3)+3))
        print("%15s(%15s)" % ("FIELD".center(15, " "),  'VALUE'.center(15, " ")))
        print("="*((15*3)+3))
        for i in self.fieldKeys():
            attr = self.__getattribute__(i)
            print("%15s(%15s)" % (str(i).center(15, " "), str(attr).center(15, " ")))

    def prepare_data(self):
        ret = {}
        for i in self.fieldKeys():
            attr = self.__getattribute__(i)
            ret[i] = attr
        return ret

    def parse_dbo(self, item:dict):
        if("_id" in item):
            self.id = item.get('_id')
        for i in self.fieldKeys():
            if(i in item):
                self.__setattr__(i, item[i])

    def delete(self):
        if not self.id:
            return
        from app import Database
        col = Database.db[self.collection]
        col.find_one_and_delete({"_id" : self.id})

    @staticmethod
    def get(obj, where : dict = {}, what : dict = None):
        spawn = obj()
        from app import Database
        col = Database.db[spawn.collection]
        if(what is not None):
            data = col.find_one(where, what)
        else:
            data = col.find_one(where)
        if(not data):
            return False
        spawn.parse_dbo(data)
        return spawn
    
    @staticmethod
    def getAll(obj, where : dict = {}, what : dict = None):
        spawn = obj()
        ret = []
        from app import Database
        col = Database.db[spawn.collection]
        if(what is not None):
            data = col.find(where, what)
        else:
            data = col.find(where)
        for i in data:
            hold = obj()
            hold.parse_dbo(i)
            ret.append(hold)
        return ret

    def init_index(self, col):
        pass

    def key_error(self):
        return "A key error occurd"

    def save(self):
        from app import Database
        import pymongo
        col = Database.db[self.collection]
        data = self.prepare_data()
        if(col.count() is 0):
            self.init_index(col)
            print("Index init complete")
        try:
            if(self.id is -1):
                resp = col.insert_one(data)
                self.id = resp.inserted_id
                print("Item inserted :",self.id)
            else:
                resp = col.update({"_id":self.id}, data)
                print("Item updated :",self.id)
        except pymongo.errors.DuplicateKeyError:
            self.ERROR = self.key_error()
            return False
        return True