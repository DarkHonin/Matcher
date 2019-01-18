from bson import ObjectId
from .dbo import Chat, Message

def spawn_chat(u1 : ObjectId, u2 : ObjectId):
    item = Chat.get_for_ids(u1, u2)
    if not item:
        item = Chat(u1, u2)
    return item
