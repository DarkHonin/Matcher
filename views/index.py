from flask.views import MethodView
from flask import request, abort, Flask, render_template, session, jsonify, redirect, url_for
from functools import wraps
from systems.properties import *
from systems.users import User, UserInfo
from systems.exceptions import SystemException

def isValidUrl(f):
    @wraps(f)
    def inner(*args, **wkargs):
        if("page" not in wkargs):
            print("Page valid")
            return f(**wkargs)    
        page = wkargs['page']
        if (page not in ["register", "login"]):
            abort(404)
        print("Page valid")
        return f(*args, **wkargs)
    return inner

class IndexView(MethodView):

    decorators = [isValidUrl, check_captcha, RequestValidator()]

    def get(self, page="login"):
        if(session['user']):
            return redirect(url_for("home"))
        if page == 'register':
            return render_template("pages/index/register.html")
        return render_template("pages/index/login.html")
        
    def post(self, page="login"):
        data = request.get_json()
        if(page == "register"):
            usr = User(data['uname'], data['email'], data['password'])
            usr.register()
            info = UserInfo(usr, data['fname'], data['lname'], "", "Prefer not to say", "Prefer not to say", "[]", [], None)
            info.save()
            return jsonify({"status" : "JOY", "actions": {"displayMessage" : "Please check your account for an activation email"}})
        else:
            usr = User.get({"uname" : data["uname"]})
            if not usr or not usr.active:
                raise SystemException("Username/Password invalid", SystemException.USER_CREATE_EXCEPTION)
            usr.login(data['password'])
        return jsonify({"status" : "JOY", "actions": {"displayMessage" : "Welcome back %s" % usr.uname, "redirect" : "/home"}})


    @classmethod
    def bind(cls, app : Flask):
        app.add_url_rule("/<page>", view_func=cls.as_view("index"))
        app.add_url_rule("/", view_func=cls.as_view("index_plain"))

        @app.route("/logout")
        def logout():
            del(session['user'])
            del(session['user_info'])
            return redirect("/login")