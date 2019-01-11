from flask import Blueprint, render_template
from app.users import User
from flask_jwt_extended import jwt_required

SEARCH_BLUEPRINT = Blueprint("search", __name__)

def search(uname, min_age=0, max_age=0):
    pass


@SEARCH_BLUEPRINT.route("/search")
@jwt_required
def view():
    return render_template("search/pages/search.html", users=User.get())