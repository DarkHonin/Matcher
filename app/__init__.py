from flask import Flask, session
from flask_socketio import SocketIO

app = Flask(__name__)
sockets = SocketIO(app)

from flask_pymongo import PyMongo
from flask_mail import Mail
from app.framework.users.SocketDispatch import UserSocketNamespace

sockets.on_namespace(UserSocketNamespace('/home'))
app.secret_key = "5bf87554084b104d3f7dbb52"
app.config.from_pyfile("instance/config.py")

Database = PyMongo(app)
Mailer = Mail(app)

from app.instance import routes
from app.framework import Page
for i in Page.PAGES:
    i.bind(app)

