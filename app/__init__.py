from flask import Flask
from flask_pymongo import PyMongo
from app.routes import Routes
from app.obj import Page
from flask_mail import Mail
from app.users import logout

app = Flask(__name__)
app.secret_key = "5bf87554084b104d3f7dbb52"
app.config.from_pyfile("instance/config.py")
for route in Routes:
    print("Loading route:", route)
    Page.bind_routes(app, route, Routes[route])

app.add_url_rule("/logout", "logout", logout)

@app.route("/test")
def test():
    from app.users import User, LookupUser
    user = LookupUser("Peach")
    #user = User()
    #user.email = "Adam"
    #user.uname = "Peach"
    user.log_fields()
    user.save()
    return "OK"

Database = PyMongo(app)
Mailer = Mail(app)
