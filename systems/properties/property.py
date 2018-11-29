import re
from systems.exceptions import SystemException
from flask import render_template
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

    def validate(self, container:dict):
        print("Checking propery %s" % (self.key))
        if (self.key not in container) and self.required:
            raise SystemException(self.errorMessage, SystemException.FIELD_ERROR)
        value = container[self.key]
        if not self.tester.match(value):
            raise SystemException(self.errorMessage, SystemException.FIELD_ERROR)
        return True

    @property
    def format(self):
        if(self.type is "enum"):
            stripped = self.regex[1:-1]
            split = stripped.rsplit("|")
            return split
        return self.regex

    def render(self, container):
        if self.type is "enum":
            return render_template("fields/enum_style.html", item=self, value=getattr(container, self.key))
        if self.type is "list":
            return render_template("fields/list_style.html", item=self, value=getattr(container, self.key))
        if self.type is "blob":
            return render_template("fields/blob_style.html", item=self, value=getattr(container, self.key))
        return render_template("fields/text_style.html", item=self, value=getattr(container, self.key))
