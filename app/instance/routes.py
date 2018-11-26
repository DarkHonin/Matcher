from app.framework import Page
from app.framework.users.Page import INSTANCE as UserPage
from app.framework import RedeemPage

Page.register(UserPage)
Page.register(RedeemPage())