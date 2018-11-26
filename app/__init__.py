from flask import Flask, session
from flask_pymongo import PyMongo
from flask_mail import Mail
from flask_sockets import Sockets

app = Flask(__name__)
app.secret_key = "5bf87554084b104d3f7dbb52"
app.config.from_pyfile("instance/config.py")

Database = PyMongo(app)
Mailer = Mail(app)

from app.instance import routes
from app.framework import Page
for i in Page.PAGES:
    i.bind(app)
