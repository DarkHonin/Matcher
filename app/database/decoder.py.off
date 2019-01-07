from flask.json import JSONDecoder
from bson.objectid import ObjectId
from . import DBDocument
import dateutil.parser
class DBDDecoder(JSONDecoder):
	def __init__(self, *args, **kwargs):
		self.original_hook = kwargs.pop("object_hook", None)
		JSONDecoder.__init__(self, *args,
			object_hook=self.handle_custom_hooks, **kwargs)

	def handle_custom_hooks(self, dct):
		if "DBID" in dct:
			return ObjectId(dct["DBID"])
		if "date" in dct:
			return dateutil.parser.parse(dct["date"])
		try:
			if "__class" in dct:
				return DBDocument.fromJSON(dct)
		except Exception as e:
			print(e)
		if (self.original_hook):
			return self.original_hook(dct)
		return dct