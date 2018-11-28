from systems.exceptions import SystemException

class UserCreateException(SystemException):
    def __init__(self, message):
        Exception.__init__(self, message)