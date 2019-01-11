from app.users import User
from app.account import Account
import json
import datetime
import random

surnames = json.load(open("bogus/Surnames.json", "r"))
m_names = json.load(open("bogus/names_m.json", "r"))
f_names = json.load(open("bogus/names_f.json", "r"))

mlen = len(m_names)
flen = len(f_names)

lipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus efficitur urna nec interdum scelerisque. Quisque tempor augue at ipsum dignissim, eget pharetra ipsum ullamcorper. Proin eu eleifend enim. Nam iaculis placerat molestie. Praesent feugiat rutrum arcu eget semper. Praesent efficitur massa eu urna bibendum, sit amet efficitur sapien molestie. Ut euismod urna quis placerat aliquam. Sed elementum nunc eu posuere laoreet. Vestibulum congue eleifend convallis."
liptag = lipsum.split(" ")
imgs = []

for e in range(0, 84):
    n = surnames[random.randint(0, len(surnames) - 1)]
    if e % 2:
        fn = m_names[random.randint(0, mlen-1)]
    else:
        fn = f_names[random.randint(0, flen-1)]
    print("making user: %s %s" % (fn, n))
    usr = User(uname=fn[:1]+n[:4], email="%s%s@email.com" % (fn, n), password="Passw0rd")
    User.activate_account(usr)
    profile = Account(usr, fname=fn, lname=n, dob=str(random.randint(1980, 2000))+"-07-06")
    profile.tags = [liptag[random.randint(0, len(liptag) - 1)] for i in range(0, 6)]
    profile.gender = ["Female", "Male"][e % 2]
    profile.interest= ["Men", "Women", "Both"][random.randint(0, 2)]
    profile.biography = lipsum
    print("Registered user ", usr.uname)
    profile.save()
    


