from flask import Blueprint, jsonify, render_template, abort, url_for, session, redirect
from jinja2 import TemplateNotFound
from api import APIMessage, APIMessageRecievedDecorator, APISuccessMessage, APIException
from users.messages import RegisterMessage, LoginMessage
from users.tokens import redeemToken
from users.user import User

from flask import Blueprint
USER_BLUEPRINT = Blueprint("user_manager", __name__)

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
    print("Logging in...")
    if not message.valid:
        raise message.errorMessage
    usr = User.get({"uname" : message.uname})
    if not usr:
        print("%s :: User does not exists" % message.uname)
        raise APIException(message="Username/password invalid")
    print("User found")
    if not usr.login(message.password):
        print("%s :: Password is wrong" % message.uname)
        raise APIException(message="Username/password invalid")
    print("Logged in")
    return APISuccessMessage(message="Welcome back %s" % message.uname, redirect=url_for("user_accounts.account_profile")).messageSend()

############################################################################################################################################################

@USER_BLUEPRINT.route("/redeem/<token>", methods=["POST"])
@APIMessageRecievedDecorator(LoginMessage)
def redeem(token, message):
    if not message.valid:
        return message.errorMessage.messageSend()
    
    login(**{})
    print("Redeeming...")
    redeemToken(token)
    return APISuccessMessage(message="Your account is now active %s" % message.uname, redirect=url_for("user_accounts.account_profile")).messageSend()

############################################################################################################################################################

@USER_BLUEPRINT.route("/<page>", methods=["GET"])
@USER_BLUEPRINT.route("/", methods=["GET"], defaults={"page" : "login"})
def index(page):
    try:
        return render_template("users/pages/%s.html"%page, submit_to=url_for("user_manager."+page))
    except TemplateNotFound:
        abort(404)

@USER_BLUEPRINT.route("/logout", methods=["GET", "POST"])
def logout():
    del(session['user'])
    return redirect(url_for("user_manager.index"))

@USER_BLUEPRINT.route("/redeem/<token>", methods=["GET"])
def redeemView(token):
    return render_template("users/pages/redeem.html", submit_to=url_for("user_manager.redeem", token=token))
