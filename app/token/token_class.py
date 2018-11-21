from app.obj import DataObject
import uuid
from datetime import datetime, timedelta

class Token(DataObject):

	EXPIRE = 5

	def __init__(self, key : dict, callback):
		DataObject.__init__(self,{
			"date"	: datetime.now(),
			"key"	: key,
			"token" : uuid.uuid1().hex,
			"callback" : callback
		}, "Tokens")

	def isValid(self):
		now = datetime.now()
		age = now - self.date['value']
		return age.days < self.EXPIRE

	def getKey(self):
		return self.key['value'].keys()[0]

	def resolve(self):
		from app.token import KEY_CLASSES
		cl = KEY_CLASSES[self.getKey()]
		id = key['value'][self.getKey()]
		print(cl, id)