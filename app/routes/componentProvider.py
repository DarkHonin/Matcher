from app.obj import Page
from app.obj import Component
import flask

class ComponentProvider(Page, Component):
    def __init__(self):
        Page.__init__(self, "/component", "Matcher::Component", methods=["POST"])
        Component.__init__(self, {
            "login" : "components/index/login.html",
            "register" : "components/index/register.html"
            })
        

    def post(self):
        self.clearRequest()
        resp = self.RESPONSE
        if(resp['status'] is "JOY"):
            resp['payload'] = flask.render_template(self.getState(self.REQUEST_JSON['id']))
        return flask.jsonify(resp)