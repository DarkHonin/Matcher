from bson import ObjectId
from .dbo import Chat

def spawn_chat(u1 : ObjectId, u2 : ObjectId):
    item = Chat.get({"author.user" : {"$elemMatch" : {"$in" : [u1, u2]}}})
    if not item:
        item = Chat(u1, u2)
    return item
