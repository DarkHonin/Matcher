from app.obj import Page

class Index(Page):
    def __init__(self):
        super(Index, self).__init__("/", "Matcher::Index")

    def get(self):
        return "index get"

    def post(self):
        return "index post"

    def all(self):
        return "index all"