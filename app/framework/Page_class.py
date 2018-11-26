from flask import Flask
"""
    The page object signifies the end point container for each route.
    
    routes => dict      Containes the route information
        eg. {
            "/home:HOME_PAGE:GET" : "render_homepage"
        }
"""

class Page:
    PAGES = []

    @staticmethod
    def register(page):
        if page not in Page.PAGES:
            Page.PAGES.append(page)

    def __init__(self, routes : dict = {}):
        self._routes = {}
        for r, f in routes.items():
            self.addRoute(r, f)

    def addRoute(self, rule : str, function):
        parts = rule.split(':')
        self._routes[parts[1]] = {
            "URL" : parts[0],
            "METHODS" : (parts[2].split(",") if len(parts) is 3 else []),
            "NAME" : parts[1],
            "FUNCTION" : function
        }
        print("Route registered: %s" %(self._routes[parts[1]]))
    
    def bind(self, app : Flask):
        for n, r in self._routes.items():
            print("Binding passive route %s::%s" % (n, r["METHODS"]))
            app.add_url_rule(r['URL'], n, r["FUNCTION"], methods=(r["METHODS"] if r["METHODS"] else None))


