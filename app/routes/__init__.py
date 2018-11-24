from app.routes.register import Register
from app.routes.user.profile import Profile
from app.routes.user.home import Home
from app.routes.login import Login
from app.routes.history import History
from app.routes.settings import Settings
from app.routes.match import Match
from app.routes.tokenRedeem import TokenRedeem

Routes = {
    "login" : Login(),
    "home" : Home(),
    "profile" : Profile(),
    "register" : Register(),
    "history" : History(),
    "settings" : Settings(),
    "match" :   Match(),
    "redeem" : TokenRedeem()
}