from flask import Blueprint, jsonify, render_template, abort
from jinja2 import TemplateNotFound

USER_BLUEPRINT = Blueprint("user_manager", __name__)

@USER_BLUEPRINT.route("/register", methods=["POST"])
def register():
    pass

@USER_BLUEPRINT.route("/login", methods=["POST"])
def login():
    return jsonify({"message" : "Hey"})

@USER_BLUEPRINT.route("/redeemToken/<token>", methods=["POST"], defaults={"token" : None})
def redeem(token):
    pass

@USER_BLUEPRINT.route("/<page>", methods=["GET"])
@USER_BLUEPRINT.route("/", methods=["GET"], defaults={"page" : "login"})
def index(page):
    try:
        print(page)
        return render_template("users/pages/%s.html"%page, submit_to="user_manager."+page)
    except TemplateNotFound:
        abort(404)

@USER_BLUEPRINT.route("/<page>", methods=["VIEW"])
@USER_BLUEPRINT.route("/", methods=["VIEW"], defaults={"page" : "login"})
def fetchView(page):
    try:
        return render_template("users/parts/%s.html"%page, submit_to="user_manager."+page)
    except TemplateNotFound:
        abort(404)