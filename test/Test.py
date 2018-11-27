from Validator_class import *

GENDER = {
        "Male" : "0",
        "Female" : "1"
}

SEXUALITY = {
	"Men"               : "0",
	"Women"             : "1",
	"Both"              : "2",
	"Prefer not to say" : "3"
}

PASSWORD_FIELD = Field("password", {}, True, "Password")
EMAIL_FIELD = Field("email", {"Invalid Email" : Validator.isEmail}, True, "Email")
UNAME_FIELD = Field("uname", {}, True, "Username")

PUBLIC_FIELDS = [
	UNAME_FIELD,
	Field("fname", {"Not a valid first name" : Validator.isValidName}, True, "First name"),
	Field("lname", {"Not a valid first name" : Validator.isValidName}, True, "Last name"),
	Field("gender", {"Not a valid gender":Validator.inDict}, False, "Gender", "enum", GENDER),
	Field("Sexuality", {"Its cool that your into that but we cant show that here":Validator.inDict}, False, "Interested in", "enum", SEXUALITY),
]

PRIVATE_FIELDS = [
	EMAIL_FIELD
]

FIELDS = PUBLIC_FIELDS + PRIVATE_FIELDS

GLOBAL_VALIDATOR = Validator(FIELDS)

data =  {'uname': 'Username', 'fname': 'First', 'lname': 'Last', 'gender': '1', 'Sexuality': '1', 'email': 'dgmon.mail@gmail.com'}
GLOBAL_VALIDATOR.validate(data)
print(GLOBAL_VALIDATOR.ERROR)