from Function import Func
from Tuple import Tuple


class Struct(Func):
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields
        self.lazy = False

    def simplify(self, program_state=None):
        return self

    def apply(self, values, program_state=None):
        if isinstance(values, Tuple):
            values = values.tup
        else:
            values = [values]
        return Structure(self, values)

    def __str__(self):
        return self.name + ' ' + ' '.join(self.fields)


class Structure:
    def __init__(self, struct, values):
        self.type = struct
        self.values = values
        self.state = dict(zip(self.type.fields, values))

    def simplify(self, program_state):
        return self

    def __str__(self):
        return ('(' + self.type.name + ' '
                + ' '.join(list(map(str, self.values))) + ')')