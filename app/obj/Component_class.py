from flask import request

class Component:
	NONE = "none"

	REQUEST_JSON = {}

	RESPONSE = {}

	def __init__(self, states : dict):
		self.states = states
		self.requestCleaners = {
			"status" : self.status 
		}

	def addCleaner(self, atr , fn):
		self.requestCleaners[atr] = fn

	def getState(self, state):
		return self.states[state]

	def clearRequest(self):
		self.REQUEST_JSON = request.get_json()
		for i in self.requestCleaners:
			self.RESPONSE[i] = self.requestCleaners[i]()

	def status(self):
		if("id" not in self.REQUEST_JSON):
			return "NOJOY"
		elif(self.REQUEST_JSON['id'] not in self.states):
			return "NOJOY"
		return "JOY"
			
			