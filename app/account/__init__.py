from .dbo import Account

def create_user_account(user, message):
	Account(user, **message.__dict__).save()
	pass