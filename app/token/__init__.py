from app.token.token_class import Token

KEY_CLASSES = {}

def AddKeyClass(key, clas):
	print("Token key class registered '%s'" % (key))
	KEY_CLASSES[key] = clas