
class DataObject:
    def __init__(self, fields : dict, collection : str):
        for i in fields:
            self.__setattr__(i, {"default" : fields[i], "value": fields[i]})
        self.field_names = fields.keys()
        self.collection = collection
        self.id = -1
        self.ERROR = False

    def log_fields(self):
        print("-"*((15*3)+3))
        print("%15s(%15s:%15s)" % ("FIELD".center(15, " "), 'DEFAULT'.center(15, " "), 'VALUE'.center(15, " ")))
        print("="*((15*3)+3))
        for i in self.field_names:
            attr = self.__getattribute__(i)
            print("%15s(%15s:%15s)" % (str(i).center(15, " "), str(attr['default']).center(15, " "), str(attr['value']).center(15, " ")))

    def setValue(self, key ,val):
        atr = self.__getattribute__(key)
        if(atr):
            atr['value'] = val

    def prepare_data(self):
        ret = {}
        for i in self.field_names:
            attr = self.__getattribute__(i)
            if(attr['value'] is not attr['default']):
                ret[i] = attr['value']
        return ret

    def parse_dbo(self, item:dict):
        if("_id" in item):
            self.id = item.get('_id')
        for i in self.field_names:
            if(i in item):
                self.__getattribute__(i)['value'] = item[i]

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
        if(col.count() is 0):
            self.init_index(col)
            print("Index init complete")
        try:
            if(self.id is -1):
                resp = col.insert_one(self.prepare_data())
                self.id = resp.inserted_id
                print("Item inserted :",self.id)
            else:
                resp = col.update({"_id":self.id}, self.prepare_data())
                print("Item updated :",self.id)
        except pymongo.errors.DuplicateKeyError:
            self.ERROR =  {"status" : "NOJOY", "message" :  self.key_error()}
            return False
        return True