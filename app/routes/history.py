from app.obj import Page

class History(Page):
    def __init__(self):
        super(History, self).__init__("/history", "Matcher::History")

    def get(self):
        return "index all"