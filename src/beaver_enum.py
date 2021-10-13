class EnumValue:
    def __init__(self, enum, name, value):
        self.type = enum.name
        self.enum = enum
        self.name = name
        self.value = value

    def simplify(self, program_state):
        return self

    def __str__(self):
        return self.name


class Enum:
    def __init__(self, name, values):
        self.name = name
        self.values = values

    def simplify(self, program_state):
        return self

    def __str__(self):
        return ' | '.join(self.values)