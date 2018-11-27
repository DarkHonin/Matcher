from app.framework.users import User
import json
import random

surnames = json.load(open("app/bogus/Surnames.json", "r"))
m_names = json.load(open("app/bogus/names_m.json", "r"))
f_names = json.load(open("app/bogus/names_f.json", "r"))

mlen = len(m_names)
flen = len(f_names)

for i, n in enumerate(surnames):
    if i > 50:
        break
    if i % 2:
        fn = m_names[random.randint(0, mlen-1)]
    else:
        fn = f_names[random.randint(0, flen-1)]
    print("making user: %s %s" % (fn, n))
    user = User()
    user.fname = fn
    user.lname = n
    user.gender = ("Male" if i % 2 else "Female")
    user.sexuality = user.SEXUALITY[random.randint(0, 2)]
    user.biography = "A random bogus bio"
    user.email = "%s%s@email.com" % (fn, n)
    user.email_valid = True
    user.active = True
    user.uname = fn[:1]+n[:4]
    user.save()
    user.password = "password"


