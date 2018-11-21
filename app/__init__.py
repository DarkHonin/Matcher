from flask import Flask
from flask_pymongo import PyMongo
from app.routes import Routes
from app.obj import Page
from flask_mail import Mail

app = Flask(__name__)
app.config.from_pyfile("instance/config.py")
for route in Routes:
    print("Loading route:", route)
    Page.bind_routes(app, route, Routes[route])

Database = PyMongo(app)
Mailer = Mail(app)
