from flask import Blueprint, jsonify, render_template, abort, url_for
from jinja2 import TemplateNotFound
from api import APIMessage, APIMessageRecievedDecorator, APISuccessMessage, APIException
from users.messages import RegisterMessage, LoginMessage
from users.tokens import redeemToken
from users.user import User

from users import USER_BLUEPRINT

############################################################################################################################################################

@USER_BLUEPRINT.route("/register", methods=["POST"])
@APIMessageRecievedDecorator(RegisterMessage)
def register(message : APIMessage):
    if not message.valid:
        return message.errorMessage
    User.registerNewUser(**(message.items))
    return APISuccessMessage(message="Please verify your email before proceeding").messageSend()

############################################################################################################################################################

@USER_BLUEPRINT.route("/login", methods=["POST"])
@APIMessageRecievedDecorator(LoginMessage)
def login(message):
    if not message.valid:
        raise message.errorMessage
    usr = User.get({"uname" : message.uname})
    if not usr:
        print("%s :: User does not exists" % message.uname)
        raise APIException(message="Username/password invalid")
    if not usr.login(message.password):
        print("%s :: Password is wrong" % message.uname)
        raise APIException(message="Username/password invalid")
    return APISuccessMessage(message="Welcome back %s" % message.uname, redirect=url_for("user_manager.index")).messageSend()

############################################################################################################################################################

@USER_BLUEPRINT.route("/redeem/<token>", methods=["POST"])
@APIMessageRecievedDecorator(LoginMessage)
def redeem(token, message):
    if not message.valid:
        return message.errorMessage.messageSend()
    login()
    redeemToken(token)
    return APISuccessMessage(message="Your account is now active %s" % message.uname, redirect=url_for("user_manager.index")).messageSend()

############################################################################################################################################################

@USER_BLUEPRINT.route("/<page>", methods=["GET"])
def index(page):
    try:
        return render_template("users/pages/%s.html"%page, submit_to=url_for("user_manager."+page))
    except TemplateNotFound:
        abort(404)

@USER_BLUEPRINT.route("/redeem/<token>", methods=["GET"])
def redeemView(token):
    return render_template("users/pages/redeem.html", submit_to=url_for("user_manager.redeem", token=token))

@USER_BLUEPRINT.route("/<page>", methods=["VIEW"])
@USER_BLUEPRINT.route("/", methods=["VIEW"], defaults={"page" : "login"})
def fetchView(page):
    try:
        return render_template("users/parts/%s.html"%page, submit_to="user_manager."+page)
    except TemplateNotFound:
        abort(404)