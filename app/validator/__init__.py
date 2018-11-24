from app.validator.Validator_class import Validator, Field

PASSWORD_FIELD = Field("password", {}, True, "Password")
EMAIL_FIELD = Field("email", {"Invalid Email" : Validator.isEmail}, True, "Email")
UNAME_FIELD = Field("uname", {}, True, "Username")