from app.obj import DataObject
import uuid
from datetime import datetime, timedelta

class Token(DataObject):

	EXPIRE = 5

	def __init__(self):
		DataObject.__init__(self,{
			"date"	: None,
			"key"	: None,
			"token" : None,
			"callback" : None
		}, "Tokens")
		self.date["value"] = datetime.now()
		self.token['value'] = uuid.uuid1().hex

	def isValid(self):
		now = datetime.now()
		age = now - self.date['value']
		return age.days < self.EXPIRE

	def getKey(self):
		return list(self.key['value'].keys())[0]

	def resolve(self):
		from app.token import KEY_CLASSES
		cl = KEY_CLASSES[self.getKey()]
		id = self.key['value'][self.getKey()]
		cl = cl.get(cl, {"_id" : id}, {"password" : 0})
		cl.__getattribute__(self.callback['value'])(self)
		self.delete()