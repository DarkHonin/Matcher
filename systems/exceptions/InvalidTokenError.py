from systems.exceptions import SystemException

class InvalidTokenError(SystemException):
    def __init__(self, message):
        SystemException.__init__(self, message, SystemException.INVALID_TOKEN)