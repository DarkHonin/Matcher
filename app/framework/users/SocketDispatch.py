import flask
from flask_socketio import Namespace, emit
class UserSocketNamespace(Namespace):

    PAGES = {
        "home" : "homePage"
    }

    def homePage(self):
        emit("show_page", flask.render_template("pages/user/home.html"))

    def on_connect(self):
        print("Connected")

    def on_my_event(self, data):
        print(data)
        emit("Responce", data)

    def on_message(self, message):
        print("Message:",message)

    def on_getMessages(self, data):
        if not self.isAuthed(data):
            return emit("error", "You need to be logged in to use this page")
        print("Get messages")

    def on_getPage(self, data):
        if not self.isAuthed(data):
            return emit("error", "You need to be logged in to use this page")
        if "page" not in data or data['page'] not in self.PAGES:
            return emit("error", "The page does not exist")
        getattr(self, self.PAGES[data["page"]])()

    def parseSocketData(self, rawData):
        print(rawData)
        import json
        data = json.loads(rawData)
        return data

    def isAuthed(self, data):
        from app.framework.users.Page import INSTANCE as UserPage
        if not UserPage.isUserLoggedIn() or "token" not in data:
            print("no user logged in")
            return False
        users = UserPage.LOGGED_USERS
        print(users[flask.session['user']]["SessionID"] , data["token"])
        if users[flask.session['user']]["SessionID"] == data["token"]:
            return True
        return False
