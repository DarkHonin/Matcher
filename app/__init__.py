from flask import Flask
from app.routes import Routes
from app.obj import Page
app = Flask(__name__)
app.config.from_pyfile("instance/config.py")

for route in Routes:
    print("Loading route:", route)
    Page.bind_routes(app, route, Routes[route])
    #app.add_url_rule(Routes[route].URL, route, Routes[route].route)
