from systems.exceptions import SystemException

class UserCreateException(SystemException):
    def __init__(self, message):
        SystemException.__init__(self, message, SystemException.USER_CREATE_EXCEPTION)