from app.framework import Page
from app.framework.users import UserPage
from app.framework import RedeemPage

Page.register(UserPage())
Page.register(RedeemPage())