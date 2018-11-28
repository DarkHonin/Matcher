import re
from systems.exceptions import SystemException

class Property:
    def __init__(self,
                key,
                label, 
                regex,
                errorMessage : str = "The field does not meet the requirements",
                fieldtype : str = 'text',
                required : bool = False):
        self.key = key
        self.label = label
        self.regex = regex
        self.tester = re.compile(regex)
        self.type = fieldtype
        self.required = required
        self.errorMessage = errorMessage

    def validate(self, container):
        value = getattr(container, self.key)
        if not value and self.required:
            raise SystemException(self.errorMessage, SystemException.FIELD_ERROR)
        elif not value:
            return False
        if not self.tester.match(value):
            raise SystemException(self.errorMessage, SystemException.FIELD_ERROR)
        return True