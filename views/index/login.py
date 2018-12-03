from flask.views import MethodView
from flask import request, abort, Flask, render_template, session, jsonify, redirect, url_for
from functools import wraps
from systems.properties import *
from systems.users import User, UserInfo, registerUser
from systems.exceptions import SystemException

class Login(MethodView):

    decorators = [check_captcha, RequestValidator()]

    def get(self):
        if("user" in session):
            return redirect(url_for("home"))
        return render_template("pages/index/login.html")
        
    def post(self, uname, password):
        usr = User.get({"uname" : uname})
        if not usr or not usr.email_valid:
            raise SystemException("Username/Password invalid", SystemException.USER_CREATE_EXCEPTION)
        usr.login(password)
        return jsonify({"status" : "JOY", "actions": {"displayMessage" : "Welcome back %s" % usr.uname, "redirect" : "/home"}})


    @classmethod
    def bind(cls, app : Flask):
        app.add_url_rule("/", view_func=cls.as_view("index"))
        app.add_url_rule("/login", view_func=cls.as_view("login"))