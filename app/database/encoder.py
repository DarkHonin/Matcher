from flask.json import JSONEncoder
from bson.objectid import ObjectId
from datetime import datetime

class DBDEncoder(JSONEncoder):
	def default(self, obj):
		from . import DBDocument
		if isinstance(obj, DBDocument):
			return obj.toJSON()
		elif isinstance(obj, ObjectId):
			return {"DBID" : str(obj)}
		elif isinstance(obj, datetime):
			return {"date" : obj.isoformat()}
		else:
			return JSONEncoder.default(self, obj)