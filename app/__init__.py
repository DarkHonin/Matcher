from flask import Flask, session, Blueprint, jsonify, request
from flask_socketio import SocketIO
from flask_pymongo import PyMongo
from flask_mail import Mail
from systems.exceptions import SystemException

app = Flask(__name__)
app.secret_key = "5bf87554084b104d3f7dbb52"
app.config.from_pyfile("instance/config.py")


Database = PyMongo(app)
Mailer = Mail(app)


sockets = SocketIO(app)

@app.errorhandler(SystemException)
def handle_error(error):
    message = [str(x) for x in error.args]
    return jsonify({"status" : "NOJOY", "actions" : {"displayMessage" : message}, "code" : error.code}), 500

@app.route("/test")
def test():
    import requests
    import sys
    url = "http://api.ipstack.com/%s?access_key=c3d5cfa1b31c8989bb9c1d4f36cc096b" % request.environ['REMOTE_ADDR']
    response = requests.get(url)
    return jsonify(response.json())


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


