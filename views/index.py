from flask.views import MethodView
from flask import request, abort, Flask, render_template
from functools import wraps
from systems.properties import check_captcha, validate_request
from systems.users import User

def isValidUrl(f):
    @wraps(f)
    def inner(**wkargs):
        if("page" not in wkargs):
            print("Page valid")
            return f(**wkargs)    
        page = wkargs['page']
        if (page not in ["/register", "/login"]):
            abort(404)
        print("Page valid")
        return f(**wkargs)
    return inner

class IndexView(MethodView):

    def get(self, page="login"):
        print(page)
        if page == 'register':
            return render_template("pages/index/register.html")
        return render_template("pages/index/login.html")
        
    def post(self, page="login"):
        print("Should be working")
        return "Sex"

    @classmethod
    def bind(cls, app : Flask):
        app.add_url_rule("/<page>", view_func=cls.as_view("index"))
        app.add_url_rule("/", view_func=cls.as_view("index_plain"))