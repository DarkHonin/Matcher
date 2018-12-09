"""
    Class :: APIMessage

    The APIMessage serves as a standarnd medium of comunication between client and server
    it is intended to contain validation functions and seamless transition from json to
    object.


    :: Magic ::

    __init__                    **kwargs : dict

        The passed dict is handled as the instnace varibales

    :: Methods ::

    validate            None

        This method is called on message send and message recieved to excecute the attibute
        validation

    messageRecieve      None

        Creates a new instance of the class element being refrenced then triggers the
        validation

    messageSend         

        Returns the json data for the message
        
"""

from flask import request, jsonify


class APIMessage:
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    @classmethod
    def messageRecieve(_class):
        data = request.get_json()
        if not data:
            data = {}
        instance = _class(**data)
        return instance

    def messageSend(self):
        return jsonify({"handle" : str(self.__class__.__name__), "data" : self.__dict__})

class APIValidatingMessage(APIMessage):

    REQUIRED = []

    def __init__(self, **kwargs):
        APIMessage.__init__(self, **kwargs)
        self.valid = True
        self.errors = {}

    def validate(self):
        for i in self.REQUIRED:
            if not hasattr(self, i):
                self.logError(i, "This field is required")
                self.valid = False
            elif not getattr(self, i).strip():
                self.logError(i, "This field is required")
                delattr(self, i)
                self.valid = False

        for k, v in self.__dict__.copy().items():
            tf = ("test_"+k).replace("-", "_")
            if hasattr(self, tf):
                if not getattr(self, tf)(v):
                    self.valid = False
                    delattr(self, k)

    def logError(self, attr, reason):
        if attr not in self.errors:
            self.errors.update({attr : []})
        self.errors[attr].append(reason)

    @property
    def items(self):
        items = self.__dict__
        items.pop("valid")
        items.pop("errors")
        return items

    @property
    def errorMessage(self):
        return APIFieldErrorMessage(**self.errors)

    @classmethod
    def messageRecieve(cl):
        instance = super(APIValidatingMessage, cl).messageRecieve()
        instance.validate()
        return instance

class APIException(Exception, APIMessage):
    def __init__(self, **kwargs):
        Exception.__init__(self)
        APIMessage.__init__(self, **kwargs)

    def messageSend(self):
        return jsonify({"handle" : str(APIException.__name__), "data" : self.__dict__})

class APISuccessMessage(APIMessage):
    pass

class APIFieldErrorMessage(APIException):
    def messageSend(self):
        return jsonify({"handle" : str(APIFieldErrorMessage.__name__), "data" : self.__dict__})
    pass

############################################################################################################################################


def APIMessageRecievedDecorator(_class = APIMessage):
    from functools import wraps
    def decorator(f):
        @wraps(f)
        def resolute(*args, **kws):
            return f(message=_class.messageRecieve(), *args, **kws)
        return resolute
    return decorator