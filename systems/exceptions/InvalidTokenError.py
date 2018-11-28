from systems.exceptions import SystemException

class InvalidTokenError(SystemException):
    def __init__(self, message):
        Exception.__init__(self, message)