from flask import Blueprint, render_template, request
from app.users import User
from app.account import Account
from app.account import Telemetry
from flask_jwt_extended import jwt_required, current_user
from dateutil import relativedelta
import datetime

SEARCH_BLUEPRINT = Blueprint("search", __name__)

def filter_byAgeGap(age_gap, ids, sort = False, tags : list = []):
    selector = {"user" : {"$in" : ids}, "$and" : [{"$where":"this.tags.length >= 5"}, {"$where":"this.images.length >= 1"}, {"$where" : "this.gender != '%s'" %Account.GENDER_UNSET}, {"$where" : "this.biography.length >= 25"}]}
    if age_gap >= 0:
        curr = Account.get({"user" : current_user._id}, {"dob" : 1})["dob"]
        min = curr - relativedelta.relativedelta(years=int(age_gap))
        max = curr + relativedelta.relativedelta(years=int(age_gap))
        selector = {**selector, **{"dob" : {"$lte" : max, "$gte" : min}}}
    if tags:
        selector = {**selector, **{"tags" : {"$all" : tags}}}
    ret = Account.get(selector, {"user" : 1, "class" : 1, "dob" : 1})
    if not ret:
        return []
    if not isinstance(ret, list):
        ret = [ret]
    if sort:
        ret.sort (key=lambda x: x.age(), reverse=True)
    ret = [x.user for x in ret]
    return ret

def filter_by_fame(fame, ids, sort = False):
    selector = {"user" : {"$in" : ids}}
    items = Telemetry.get(selector)
    if not items:
        return []
    if not isinstance(items, list):
        items = [items]
    if fame>= 0:
        if not isinstance(items, list):
            items = [items]
        for x in items.copy():
            if x.fame() < fame:
                items.remove(x)
    else:
        if sort:
            items.sort(key=lambda x: x.fame(), reverse=True)
    ret = [x.user for x in items]
    return ret

def search(uname=None, age_gap = -1, fame=-1, location_region=None, location_city=None, sort_by=None, tags=None):
    selector = {"active" : True}
    if uname:
        selector["uname"] = {"$regex" : ".*"+uname+".*", '$options' : 'i'}
    if location_region:
        selector["login_location.region_name"] = location_region
    if location_city:
        selector["login_location.city"] = location_city
    ret = User.get(selector, {"uname" : 1, "class" : 1, "login_location" : 1})
    if not ret:
        return []
    if not isinstance(ret, list):
        ret = [ret]
    if sort_by == "Location":
        print("Location sort")
        ret.sort(key=lambda x: (x.login_location["regeion_name"] if hasattr(x, "login_location") and x.login_location else False))
    if not isinstance(ret, list):
        ret = [ret]
    ret = [x._id for x in ret]
    ret = filter_byAgeGap(int(age_gap), ret, sort_by=="Age gap", (tags.split(", ") if tags else []))
    ret = filter_by_fame(int(fame), ret, sort_by == "Fame")
    ret = User.get({"_id" : {"$in" : ret}})
    if not ret:
        return []
    if not isinstance(ret, list):
        ret = [ret]
    if sort_by=="Name":
        ret.sort(key=lambda x: x.uname)
    return ret


@SEARCH_BLUEPRINT.route("/search")
@jwt_required
def view():
    items = search(**(request.args))
    print(">>>>",items)
    return render_template("search/pages/search.html", users=items, **(request.args))