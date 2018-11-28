from flask import Flask, session, Blueprint, jsonify
from flask_socketio import SocketIO
from flask_pymongo import PyMongo
from flask_mail import Mail
from systems.exceptions import SystemException

app = Flask(__name__)
app.secret_key = "5bf87554084b104d3f7dbb52"
app.config.from_pyfile("instance/config.py")


Database = PyMongo(app)
Mailer = Mail(app)

from app.framework.users.SocketDispatch import UserSocketNamespace
sockets = SocketIO(app)
sockets.on_namespace(UserSocketNamespace('/home'))

errors = Blueprint('errors', __name__)

@app.errorhandler(SystemException)
def handle_error(error):
    message = [str(x) for x in error.args]
    return jsonify({"status" : "NOJOY", "message" : message, "code" : error.code}), 500

from views import VIEWS
for view in VIEWS:
    print("Binding %s" % view)
    view.bind(app)

"""
from app.instance import routes
from app.framework import Page
for i in Page.PAGES:
    i.bind(app)

@app.route("/loadBogusUsers")
def bogus():
    from app.bogus import load_bogus
    return "Loaded bogus users"
"""


