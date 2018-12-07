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

    def validate(self):
        pass

    @classmethod
    def messageRecieve(_class):
        instance = _class. (request.get_json())
        instance.validate()
        pass

    def messageSend(self):
        return jsonify(self.__dict__)