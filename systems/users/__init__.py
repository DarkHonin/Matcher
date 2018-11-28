from systems.users.user import User
from systems.properties import EMAIL, USERNAME, FIRSTNAME, LASTNAME

FIELDS = {
    EMAIL.key:EMAIL,
    USERNAME,
    FIRSTNAME,
    LASTNAME
}

def registerUser