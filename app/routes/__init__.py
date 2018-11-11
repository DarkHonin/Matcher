from app.routes.index import Index
from app.routes.user import User
from app.routes.login import Login
from app.routes.history import History
from app.routes.settings import Settings
from app.routes.match import Match

Routes = {
    "index" : Index(),
    "user" : User(),
    "login" : Login(),
    "history" : History(),
    "settings" : Settings(),
    "match" :   Match()
}