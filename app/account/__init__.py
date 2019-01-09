from .dbo import Account, Telemetry

def create_user_account(user, message):
	Account(user, **message.__dict__).save()
	pass