from users.user import User
from users.profile import Profile
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
imgs = ["2018_12_11_28_0_5c10d40cddbbbe3bb4436777.jpg", "2018_12_1_27_4_5c10476b084b10931936c2fc.jpg", "2018_12_11_31_18_5c10d53bddbbbe3bb443677b.jpg"]

for e in range(0, 50):
    n = surnames[random.randint(0, len(surnames) - 1)]
    if e % 2:
        fn = m_names[random.randint(0, mlen-1)]
    else:
        fn = f_names[random.randint(0, flen-1)]
    print("making user: %s %s" % (fn, n))
    usr = User(fn[:1]+n[:4], "%s%s@email.com" % (fn, n), "Passw0rd")
    usr.activate()
    profile = Profile(usr, fn, n, str(random.randint(1980, 2000))+"-07-06")
    profile.tags = [liptag[random.randint(0, len(liptag) - 1)] for i in range(0, 6)]
    profile.gender = ["Female", "Male"][e % 2]
    profile.interest= ["Men", "Women", "Both"][random.randint(0, 2)]
    profile.biography = lipsum
    profile.images.append(imgs[random.randint(0, 2)])
    print("Registered user ", usr.uname)
    profile.save()
    


