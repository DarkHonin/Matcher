from flask import Blueprint, render_template, request
from app.users import User
from app.account import Account
from app.account import Telemetry
from flask_jwt_extended import jwt_required, current_user
from dateutil import relativedelta
import datetime

SEARCH_BLUEPRINT = Blueprint("search", __name__)
"""
    TO-DO:
        Location filtering ~ as string
        Interest Tags      ~ as array?
"""


def search(uname=None, age_gap = -1, fame=0, location_region=None, location_city=None):
    selector = {}
    if int(age_gap) >= 0:
        curr = Account.get({"user" : current_user._id}, {"dob" : 1})["dob"]
        min = curr - relativedelta.relativedelta(years=int(age_gap))
        max = curr + relativedelta.relativedelta(years=int(age_gap))
        selector = {"dob" : {"$lte" : max, "$gte" : min}}
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
    if location_region:
        selector["location.region_name"] = location_region
    if location_city:
        selector["location.city"] = location_city
    return User.get(selector, {"uname" : 1, "class" : 1})


@SEARCH_BLUEPRINT.route("/search")
@jwt_required
def view():
    items = search(**(request.args))
    if not isinstance(items, list) and items:
        items = [items]
    return render_template("search/pages/search.html", users=items, **(request.args))