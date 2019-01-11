from flask import Blueprint, render_template, request
from app.users import User
from app.account import Account
from app.account import Telemetry
from flask_jwt_extended import jwt_required
from dateutil import relativedelta
import datetime

SEARCH_BLUEPRINT = Blueprint("search", __name__)
"""
    TO-DO:
        Location filtering ~ as string
        Interest Tags      ~ as array?
"""


def search(uname=None, min_age=None, max_age=None, fame=0):
    selector = {}
    curr = datetime.datetime.now()
    if min_age:
        rel = curr - relativedelta.relativedelta(years=int(min_age))
        print(rel)
        dt = rel
        selector = {**selector, **{"dob" : {"$lte" : dt}}}
    if max_age:
        dt = datetime.datetime.now() - datetime.timedelta(days=int(max_age)*365)
        selector = {**selector, **{"dob" : {"$gte" : dt}}}
    print(selector)
    items = Account.get(selector, {"user" : 1})
    if not items:
        return []
    if not isinstance(items, list):
        items = [items]
    ids = [ x["user"] for x in items]

    telem = Telemetry.get({"user" : {"$in" : ids}})
    if not isinstance(telem, list):
        telem = [telem]
    ids = []
    for x in telem:
        print(x.fame())
        if x.fame() >= int(fame):
            ids.append(x.user)
    selector = {"_id" : {"$in" : ids}}
    if uname:
        selector["uname"] = {"$regex" : ".*"+uname+".*", '$options' : 'i'}
    return User.get(selector, {"uname" : 1, "class" : 1})


@SEARCH_BLUEPRINT.route("/search")
@jwt_required
def view():
    items = search(**(request.args))
    if not isinstance(items, list) and items:
        items = [items]
    return render_template("search/pages/search.html", users=items, **(request.args))