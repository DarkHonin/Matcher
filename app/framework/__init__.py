from app.framework.DBO_class import DataObject
from app.framework.Page_class import Page
from app.framework.validator import Validator
from app.framework.Token import Token, RedeemPage
from app.framework.JSON_responce import JsonResponce

KEY_CLASSES = {}

def AddKeyClass(key, clas):
	print("Token key class registered '%s'" % (key))
	KEY_CLASSES[key] = clas