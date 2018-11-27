import flask
from flask_socketio import Namespace, emit
class UserSocketNamespace(Namespace):

    PAGES = {
        "home" : "homePage",
        "profile" : "profilePage",
        "profile_edit" : "edit_profile"
    }

    def homePage(self):
        emit("show_page", flask.render_template("pages/user/home.html"))

    def profilePage(self):
        print("Serving profile page")
        from app.framework.users.Page import INSTANCE as UserPage
        emit("show_page", flask.render_template("pages/user/profile.html", user=UserPage.getCurrentUser(), user_current=True))

    def edit_profile(self):
        print("Serving profile edit page")
        from app.framework.users.Page import INSTANCE as UserPage
        emit("show_page", flask.render_template("pages/user/profile_edit.html", user=UserPage.getCurrentUser(), user_current=True))

    def on_connect(self):
        print("Connected")

    def on_my_event(self, data):
        print(data)
        emit("Responce", data)

    def on_saveData(self, data):
        from app.framework.users.Page import INSTANCE as UserPage
        print(data)
        if not self.isAuthed(data):
            return emit("error", "You need to be logged in to edit these settings")
        user = UserPage.LOGGED_USERS[flask.session['user']]["User"]
        if(not user.GLOBAL_VALIDATOR.validate(data["data"])):
            return emit("error", user.GLOBAL_VALIDATOR.ERROR)
        if(user.email is not data['data']['email']):
            from app.framework.users import sendActivteionEmail
            user.parse_dbo(data['data'])
            user.email_valid = False
            sendActivteionEmail(user)
        else:
            user.parse_dbo(data['data'])
        user.save()

        emit("error", "Your info has been saved")
        emit("show_page", flask.render_template("pages/user/profile.html", user=user, user_current=True))
        
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
        if users[flask.session['user']]["SessionID"] == data["token"]:
            return True
        return False
