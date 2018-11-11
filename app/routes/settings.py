from app.obj import Page
from flask import request

class Settings(Page):
    def __init__(self):
        super(Settings, self).__init__("/settings", "Matcher::Settings", methods=["GET", "POST"])

    def get(self):
        return "user get"

    def post(self):
        return "POSTED"
