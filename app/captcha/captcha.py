from app.obj import Validator

class Captcha(Validator):
	def __init__(self):
		Validator.__init__(self, {
                
                })


	def validate(self, data):
		super.validate(data)