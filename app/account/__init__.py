from .dbo import Account, Telemetry

def create_user_account(user, message):
	Account(user, **message.__dict__).save()
	pass

def get_all_tags():
	query = Account.collection().find({}, {"tags" : 1}).distinct("tags")
	return query