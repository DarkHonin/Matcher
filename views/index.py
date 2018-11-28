from flask.views import MethodView
from flask import request, abort, Flask, render_template
from functools import wraps

from systems.users import User

def isValidUrl(f):
    @wraps(f)
    def inner(**wkargs):
        if("page" not in wkargs):
            return f(**wkargs)    
        page = wkargs['page']
        if (page not in ["register", "login"]):
            abort(404)
        return f(**wkargs)
    return inner

class IndexView(MethodView):

    decorators = [isValidUrl]

    def get(self, page):
        print(page)
        if page == 'register':
            return render_template("pages/index/register.html")
        return render_template("pages/index/login.html")
        
    def post(self, page="login"):
        pass

    def view(self, page="login"):
        pass

    @classmethod
    def bind(cls, app : Flask):
        app.add_url_rule("/<page>", view_func=cls.as_view("index"))
        app.add_url_rule("/", view_func=cls.as_view("index_plain"))