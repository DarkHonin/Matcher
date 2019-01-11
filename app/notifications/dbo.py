from app.database import DBDocument
from app.users import User


class Notification(DBDocument):
	pass


class UserNotifications(DBDocument):

	collection_name = "Notifications"

	def __init__(self, user : User):
		DBDocument.__init__(self)
		self.user = user._id
