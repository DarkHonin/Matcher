from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, current_user
from app.users import User
from app.account import Account

MATCHING = Blueprint("matching", __name__)

@MATCHING.route("/match")
@jwt_required
def view():
    users = get_users()
    #users = filter_by_sexuality(users)
    return jsonify(str(users))

def get_users():
    users = User.get({"active" : True, "login_location.region_name" : {"$ne" : None}})
    print("Sorting by region")
    for i in users[:5]:
        print (i.login_location)
    users.sort(key = lambda x: x.login_location["region_name"] == current_user.login_location["region_name"])
    print("Got users")
    return users

def filter_by_sexuality(users : list):
    crit = Account.get({"user" : current_user._id})

    ids = [x._id for x in users]

    if crit.interest == Account.INTEREST_BOTH:
        print("Interes in both")
        items = Account.get({"_id" : {"$in" : ids}})
    elif crit.interest == Account.INTEREST_MEN:
        items = Account.get({"_id" : {"$in" : ids}, "$and" : [
            {"gender" : {"$in" : [Account.GENDER_MALE]}},
            {"interest" : {"$in" : [crit.gender, Account.INTEREST_BOTH]}},
            {"tags" : {"$all" : crit.tags}}
        ]})
    elif crit.interest == Account.INTEREST_WOMEN:
        items = Account.get({"_id" : {"$in" : ids}, "$and" : [
            {"gender" : {"$in" : [Account.GENDER_FEMALE]}},
            {"interest" : {"$in" : [crit.gender, Account.INTEREST_BOTH]}},
            {"tags" : {"$all" : crit.tags}}
        ]})

    if not items:
        return []
    if not isinstance(items, list):
        return [q.user for q in [items]]