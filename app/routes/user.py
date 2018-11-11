from app.obj import Page
from flask import request

class User(Page):
    def __init__(self):
        super(User, self).__init__("/user/<uname>", "Matcher::User")

    def get(self):
        return "user get"
