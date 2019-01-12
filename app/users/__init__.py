from .dbo import User

def list_regions():
	query = User.collection().find({}, {"location" : 1}).distinct("location")
	region = []
	city = []
	print(query)
	for i in query:
		city.append(i["city"])
		region.append(i["region_name"])

	return region, city