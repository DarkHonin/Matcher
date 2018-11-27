from Validator_class import *
PASSWORD_FIELD = Field("password", {}, True, "Password")
EMAIL_FIELD = Field("email", {"Invalid Email" : Validator.isEmail}, True, "Email")
UNAME_FIELD = Field("uname", {}, True, "Username")

GENDER = [
            "Male",
            "Female"
        ]

SEXUALITY = [
	"Men"               ,
	"Women"             ,
	"Both"              ,
	"Prefer not to say" 
]

PUBLIC_FIELDS = [
	Field("biography", {}, False, "Biography", "blob"),
	UNAME_FIELD,
	Field("fname", {"Not a valid first name" : Validator.isValidName}, True, "First name"),
	Field("lname", {"Not a valid first name" : Validator.isValidName}, True, "Last name"),
	Field("gender", {"Not a valid gender":Validator.oneOf}, False, "Gender", "enum", GENDER),
	Field("sexuality", {"Its cool that your into that but we cant show that here":Validator.oneOf}, False, "Interested in", "enum", SEXUALITY),
]

PRIVATE_FIELDS = [
	EMAIL_FIELD,
	PASSWORD_FIELD
]

FIELDS = PUBLIC_FIELDS + PRIVATE_FIELDS

GLOBAL_VALIDATOR = Validator(FIELDS)

data =  {'uname': 'Username', 'fname': 'First', 'lname': 'Last', 'gender': 'Male', 'Sexuality': 'Men', 'email': 'dgmon.mail@gmail.com', "password" : ""}
GLOBAL_VALIDATOR.validate(data)
print(GLOBAL_VALIDATOR.ERROR)