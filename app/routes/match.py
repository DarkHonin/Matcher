from app.obj import Page
from flask import request

class Match(Page):
    def __init__(self):
        super(Match, self).__init__("/settings", "Matcher::Settings", methods=["GET", "POST"])

    def get(self):
        return "user get"

    def post(self):
        return "POSTED"
