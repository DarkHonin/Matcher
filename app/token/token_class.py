from app.obj import DataObject
import uuid
from datetime import datetime, timedelta

class Token(DataObject):

	EXPIRE = 5

	def __init__(self, key : dict =None, callback : str =None):
		DataObject.__init__(self, "Tokens")
		self.date = datetime.now()
		from app import app
		if(app.config["TESTING"]):
			self.token =app.config["TESTING_TOKEN"]
		else:
			self.token = uuid.uuid1().hex
		self.key = key
		self.callback = callback

	def fieldKeys(self):
		return [
			"date"	,
			"key"	,
			"token" ,
			"callback" 
		]

	def isValid(self):
		now = datetime.now()
		age = now - self.date
		return age.days < self.EXPIRE

	def getKey(self):
		return list(self.key.keys())[0]

	def resolve(self):
		from app.token import KEY_CLASSES
		cl = KEY_CLASSES[self.getKey()]
		id = self.key[self.getKey()]
		cl = cl.get(cl, {"_id" : id}, {"password" : 0})
		cl.__getattribute__(self.callback)(self)
		#self.delete()
		return cl