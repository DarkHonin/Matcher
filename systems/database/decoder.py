from flask.json import JSONDecoder
from bson.objectid import ObjectId
from systems.database import DBDocument

class DBDDecoder(JSONDecoder):
	def __init__(self, *args, **kwargs):
		self.original_hook = kwargs.pop("object_hook", None)
		JSONDecoder.__init__(self, *args,
			object_hook=self.handle_custom_hooks, **kwargs)

	def handle_custom_hooks(self, dct):
		if "DBID" in dct:
			return ObjectId(dct["DBID"])
		if "__class" in dct:
			return DBDocument.fromJSON(dct)
		if (self.original_hook):
			return self.original_hook(dct)
		return dct