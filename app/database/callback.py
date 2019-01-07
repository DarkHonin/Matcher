from .dbdocument import DBDocument
import importlib

class Callback(DBDocument):
	def __init__(self,method, module=None, cls=None):
		DBDocument.__init__(self)
		self.method = method
		self.module = module
		self.cls = cls

	def resolve(self):
		mod = globals()
		if self.module:
			mod = importlib.import_module(self.module).__dict__
		if self.cls:
			mod = mod[self.cls].__dict__
		ret = mod[self.method]
		if isinstance(ret, staticmethod):
			ret = ret.__func__
		return ret
