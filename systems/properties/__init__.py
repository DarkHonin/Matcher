from systems.properties.property import Property

USERNAME = Property("uname", "Username", r"^[a-zA-Z0-9]+\Z", "The username can only be alphanumerical", required=True)
EMAIL = Property("email", "Email", r"^[a-zA-Z0-9_\.\-]+@[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+$", "Please enter a valid email", required=True)
FIRSTNAME = Property("fname", "Firstname", r"^[A-Z][a-z]+$", "A name must start with one capital letter and is only alphabetical", required=True)
LASTNAME = Property("lname", "Lastname", r"^[A-Z][a-z]+$", "A name must start with one capital letter and is only alphabetical", required=True)