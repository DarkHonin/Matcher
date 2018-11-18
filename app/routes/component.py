from app.obj import Page

class Component(Page):
    def __init__(self):
        super(Component, self).__init__("/Component", "Matcher::Component")

    def get(self):
        return "Component all"