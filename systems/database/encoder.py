from flask.json import JSONEncoder
from bson.objectid import ObjectId

class DBDEncoder(JSONEncoder):
	def default(self, obj):
		from systems.database import DBDocument
		if isinstance(obj, DBDocument):
			return obj.toJSON()
		elif isinstance(obj, ObjectId):
			return {"DBID" : str(obj)}
		else:
			return JSONEncoder.default(self, obj)