from bson import ObjectId

def check_mutual_like(u1 : ObjectId, u2 : ObjectId):
    from app.account import Telemetry
    a = Telemetry.get({"user" : u1})
    b = Telemetry.get({"user" : u2})
    if u1 in b.liked_by and u2 in a.liked_by:
        print("Mutual like is confermd")
        pass # mutual like is confermed