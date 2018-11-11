from app.obj import Page

class Login(Page):
    def __init__(self):
        super(Login, self).__init__("/login", "Matcher::Welcome", methods=["POST", "GET"])

    def get(self):
        return "login get"

    def post(self):
        return "login post"