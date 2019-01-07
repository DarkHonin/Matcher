from . import DBDocument

class Editor:
	def __init__(self, subject : DBDocument):
		self.subject = subject
		

	def edit(self, key, value):
		val = prepare(key, value)
		self.subjec

	def prepare(self, key : str, value):
		ret = value
		if hasattr("prepare_"+key):
			ret = getattr("prepare_"+key, value)
		return ret