from users.user import User
import json
import datetime
import random
from users.tokens import redeemToken

surnames = json.load(open("app/bogus/Surnames.json", "r"))
m_names = json.load(open("app/bogus/names_m.json", "r"))
f_names = json.load(open("app/bogus/names_f.json", "r"))

mlen = len(m_names)
flen = len(f_names)

lipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus efficitur urna nec interdum scelerisque. Quisque tempor augue at ipsum dignissim, eget pharetra ipsum ullamcorper. Proin eu eleifend enim. Nam iaculis placerat molestie. Praesent feugiat rutrum arcu eget semper. Praesent efficitur massa eu urna bibendum, sit amet efficitur sapien molestie. Ut euismod urna quis placerat aliquam. Sed elementum nunc eu posuere laoreet. Vestibulum congue eleifend convallis."
liptag = lipsum.split(" ")


for e in range(0, 50):
    n = surnames[random.randint(0, len(surnames) - 1)]
    if e % 2:
        fn = m_names[random.randint(0, mlen-1)]
    else:
        fn = f_names[random.randint(0, flen-1)]
    print("making user: %s %s" % (fn, n))
    User.registerNewUser(uname=fn[:1]+n[:4], email="%s%s@email.com" % (fn, n), fname=fn, lname=n, dob=str(random.randint(1980, 2000))+"-07-06", password="Passw0rd", **{"g-recaptcha-response" : "heck"})
    print("Registered user ", fn[:1]+n[:4])
    redeemToken("this_is_a_testing_token")
    """tgs = []
    for i in range(0, 6):
        tgs.append(liptag[random.randint(0, len(liptag) - 1)])
    user.info = UserInfo(fn, n)
    user.info._tags = tgs
    user.info.location = [random.randint(0, 500), random.randint(0, 500)]
    user.info.interest = ["Men", "Women", "Both"][random.randint(0, 2)]
    user.info.gender = ("Male" if e % 2 else "Female")
    user.info.biography = "This is a bogus bio"
    user.info.images = ["2018_11_12_7_21_5bffab58ddbbbea8b7b49243.jpg"]
    user.validate_email()
    user.activate()"""
    


