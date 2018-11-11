from flask import Flask

class Page:
    def __init__(self, url, title, methods : list = ["GET"]):
        self.URL = url
        self.TITLE = title
        self.METHODS = methods

    @staticmethod
    def bind_routes(app : Flask, pn : str, p):
        for i in p.METHODS:
            print("Binding method:",i,"in",p)
            app.add_url_rule(p.URL, pn+"_"+i, getattr(p, i.lower()), methods=[i])

    def all(self):
        pass