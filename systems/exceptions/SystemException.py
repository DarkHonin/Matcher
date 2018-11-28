class SystemException(Exception):

    UNKOWN_ERROR = 0
    USER_CREATE_EXCEPTION = 1
    INVALID_TOKEN = 2
    FIELD_ERROR = 3


    def __init__(self, message, code):
        Exception.__init__(self, message)
        self.code = code