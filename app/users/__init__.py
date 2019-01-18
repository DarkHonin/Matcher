from .dbo import User

def list_regions():
	query = User.collection().find({}, {"login_location" : 1}).distinct("login_location")
	region = []
	city = []
	print(query)
	for i in query:
		if i:
			city.append(i["city"])
			region.append(i["region_name"])

	return region, city