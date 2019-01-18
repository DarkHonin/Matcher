from app.database import DBDocument, Editor
from datetime import datetime
from app.users import User
from app.chat import spawn_chat


class Telemetry(DBDocument):

	collection_name = "Telemetry"

	def __init__(self, user : User):
		DBDocument.__init__(self)
		self.user = user._id
		self.blocked = []
		self.liked_by = []
		self.viewed_by = []

	def block(self, blocked_user : User):
		if blocked_user._id not in self.blocked:
			self.blocked.append(blocked_user._id)
		else:
			self.blocked.remove(blocked_user._id)

	def like(self, liking_user : User):
		if liking_user._id not in self.liked_by:
			chat = spawn_chat(self.user, liking_user._id)
			if chat.accept(liking_user._id):
				from app.notifications import Notification, UserNotifications
				note = Notification(User.get({"_id" : self.user}), User.get({"_id" : liking_user._id}), Notification.ACTION_LINKED)
				UserNotifications.notify(note)
				note = Notification(liking_user, User.get({"_id" : self.user}), Notification.ACTION_LINKED)
				UserNotifications.notify(note)
				pass #mutual like
			chat.save()
			self.liked_by.append(liking_user._id)
	
	def view(self, viewing_user : User):
		if viewing_user._id not in self.viewed_by:
			self.viewed_by.append(viewing_user._id)

	def fame(self):
		if not self.viewed_by:
			return 0
		return int((len(self.liked_by) / len(self.viewed_by)) * 100)

class Account(DBDocument):

	collection_name = "Accounts"

	GENDER_MALE = "Male"
	GENDER_FEMALE = "Female"
	GENDER_UNSET = "Unknown"

	INTEREST_UNSET = "Unknown"
	INTEREST_MEN = "Men"
	INTEREST_WOMEN = "Women"
	INTEREST_BOTH = "Men & Women"

	def __init__(self, user : User, **kwargs):
		DBDocument.__init__(self)
		Telemetry(user).save()
		self.user = user._id
		self.fname = kwargs["fname"]
		self.lname = kwargs["lname"]
		self.gender = self.GENDER_UNSET
		self.interest = self.INTEREST_UNSET
		self.dob = datetime.strptime(kwargs["dob"], "%Y-%m-%d")
		self.tags = []
		self.images = []
		self.biography = ""

	@property
	def complete(self):
		if len(self.biography) < 25 or self.gender == self.GENDER_UNSET or self.interest == self.INTEREST_UNSET or len(self.tags) < 5 or not self.images:
			return False
		return True

	def age(self):
		return datetime.now().year - self.dob.year

	@property
	def problems(self):
		ret = []
		if self.gender == self.GENDER_UNSET:
			ret.append("Please select your gender")
		if self.interest == self.INTEREST_UNSET:
			ret.append("Please select your 'interest'")
		if len(self.tags) < 5:
			ret.append("Please select atelast 5 tags")
		if not self.images:
			ret.append("Your profile needs atleast 1 image")
		if len(self.biography) < 25:
			ret.append("Your biography must contain atleast 25 characters")
		return ret