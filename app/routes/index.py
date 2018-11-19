from app.obj import Page
from app.obj import Component
import flask

class Index(Page, Component):
    def __init__(self):
        Page.__init__(self, ["/", "/login", "/register"], "Matcher::Welcome", methods=["GET", "POST"])
        Component.__init__(self, {"/login" : {
            "#display" : {
                "action"    : "load",
                "url"       : "/component",
                "params"    : {"id" : "login"}
            }
        },
            "/register" : {
                "#display" : {
                    "action"    : "load",
                    "url"       : "/component",
                    "params"    : {"id" : "register"}
                }
            }
        })
        self.state = "/login"

    def get(self):
        path = flask.request.path
        if(path != "/"):
            self.state = path
        return flask.render_template("template.html", page=self)

    def post(self):
        self.clearRequest()
        resp = self.RESPONSE
        if(resp['status'] == "JOY"):
            resp['payload'] = self.getState(self.REQUEST_JSON['id'])
        return flask.jsonify(resp)
