class Union:
    def __init__(self, name, types):
        self.name = name
        self.types = types.items

    def __str__(self):
        tup = []
        for type_ in self.types:
            tup.append(str(type_))

        string = ' | '.join(tup)

        return '(' + string + ')'

    def simplify(self, program_state):
        return self