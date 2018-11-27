from app.framework.validator.Validator_class import Validator, Field

PASSWORD_FIELD = Field("password", {}, True, "Password", "password")
EMAIL_FIELD = Field("email", {"Invalid Email" : Validator.isEmail}, True, "Email")
UNAME_FIELD = Field("uname", {}, True, "Username")