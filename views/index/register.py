from flask.views import MethodView
from flask import request, abort, Flask, render_template, session, jsonify, redirect, url_for
from functools import wraps
from systems.properties import *
from systems.users import User, UserInfo, registerUser
from systems.exceptions import SystemException

class Register(MethodView):

    decorators = [check_captcha, RequestValidator()]

    def get(self):
        if("user" in session):
            return redirect(url_for("home"))
        return render_template("pages/index/register.html")
        
    def post(self, uname, password, fname, lname, email, dob):
        registerUser(uname,email,fname,lname, password, dob)
        return jsonify({"status" : "JOY", "actions": {"displayMessage" : "Please check your account for an activation email"}})

    @classmethod
    def bind(cls, app : Flask):
        app.add_url_rule("/register", view_func=cls.as_view("register"))