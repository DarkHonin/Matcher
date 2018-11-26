import flask

class JsonResponce:
	def __init__(self):
		self.state = "JOY"
		self.actions = {}

	def action(self, action, data, state=None):
		self.actions[action] = data
		if state:
			self.state = state

	def render(self):
		return flask.jsonify({"status" : self.state, "actions" : self.actions})