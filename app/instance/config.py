DEBUG = True

MAIL_FROM_EMAIL= "noreply@Matcher.co.za"

MONGO_URI = "mongodb://localhost:27017/Matcher"

MAIL_DEFAULT_SENDER = "noreplay@matcher.com"
MAIL_SERVER='smtp.gmail.com'
MAIL_PORT=465
MAIL_USE_SSL=True
MAIL_USERNAME = 'matcher.wgourley@gmail.com'
MAIL_PASSWORD = 'P4ssw0rd!'

CAPTCHA_SECRET = "6LfKuH0UAAAAAG2xrRHLq4U_STVk39jKJtp00rG8"
CAPTCHA_DISABLE = True
TESTING_APP = True
TESTING_TOKEN = "this_is_a_testing_token"

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

IGNORE_SMTP_CONNECT_ERROR = True