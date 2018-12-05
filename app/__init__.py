from flask import Flask, session, Blueprint, jsonify, request, render_template
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

@app.route("/bogus")
def bogus():
    import app.bogus.load_bogus
    return "Bogus users loaded"

@app.route("/error/<error>")
def error(error):
    return render_template("pages/error.html", err=error, txt=error[:2].upper())

from views import VIEWS
for view in VIEWS:
    print("Binding %s" % view)
    view.bind(app)

from systems.database import DBDEncoder, DBDDecoder

app.json_encoder = DBDEncoder
app.json_decoder = DBDDecoder

@app.route("/test")
def test():
    from systems.users import registerUser, User
    #registerUser("Username", "email@email.com", "First", "Last", "Passw0rd")
    return jsonify(User.get())

@app.route("/testEncode")
def endode():
    from systems.users import registerUser, User
    item = User.get()[0]
    item.telemetry.postMessage("A test", 0)
    item.save()
    return jsonify(item.encodeDocument())

