from tuple import Tuple
from types import Bool


class Collection:
    def __init__(self, items=[], operator=None):
        self.items = items
        self.operator = operator

    def simplify(self, program_state):
        if self.operator.name == ',':
            return Tuple(list(filter(lambda item: item is not None, self.items)),
                         program_state)

        if len(self.items) == 2:
            left = self.items[0]
            if left: left = left.simplify(program_state)
            right = self.items[1]
            if right:
                right = right.simplify(program_state)
            return self.operator.apply(left, right, program_state)

        for i in range(len(self.items) - 1):
            if (not self.operator.apply(self.items[i].simplify(program_state),
                                        self.items[i + 1].simplify(program_state),
                                        program_state).value):
                return Bool(False)

        return Bool(True)

    def __str__(self):
        string = list(map(str, self.items))
        return '(' + (' ' + self.operator.name + ' ').join(string) + ')'