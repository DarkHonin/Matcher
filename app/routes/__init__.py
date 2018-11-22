from app.routes.register import Register
from app.routes.user import User
from app.routes.login import Login
from app.routes.history import History
from app.routes.settings import Settings
from app.routes.match import Match
from app.routes.tokenRedeem import TokenRedeem

Routes = {
    "login" : Login(),
    "user" : User(),
    "register" : Register(),
    "history" : History(),
    "settings" : Settings(),
    "match" :   Match(),
    "redeem" : TokenRedeem()
}