# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 14:51:39 2020

@author: rohan
"""
from Tuple import Tuple
from HFunction import Func


class Variable:
    def __init__(self, name):
        self.name = name

    def simplify(self, program_state):
        if self.name == '_ ...':
            return self

        frameStack = program_state.frame_stack
        for curr in frameStack[::-1]:
            if self.name in list(curr.keys()):
                try:
                    return curr[self.name].simplify(program_state)
                except:
                    print("Variable: ", self.name)

        # raise Exception('Variable', self.name, 'is not defined')
        # print(self.name)
        return self

    def __str__(self):
        return self.name


class Type(Func):
    def __init__(self, name, expr=None, program_state=None):
        self.name = name
        self.expr = expr
        self.lazy = True
        self.program_state = program_state

    def simplify(self, program_state):
        return self

    def apply(self, var, program_state=None):
        from Operator_Functions import (default_int, default_float, default_bool,
                                        default_char)
        if self.name == 'int':
            return default_int(var, self.program_state)
        elif self.name == 'float':
            return default_float(var, self.program_state)
        elif self.name == 'bool':
            return default_bool(var, self.program_state)
        elif self.name == 'char':
            return default_char(var, self.program_state)

        return Null()

    def __str__(self):
        return str(self.expr)


class Null:
    def __init__(self):
        self.value = None

    def __str__(self):
        return '?'

    def simplify(self, program_state):
        return self


class Int:
    def __init__(self, value):
        self.type = 'int'
        self.value = value

    def simplify(self, program_state):
        return self

    def __str__(self):
        return str(self.value)


class Float:
    def __init__(self, value):
        self.type = 'float'
        self.value = value

    def simplify(self, program_state):
        return self

    def __str__(self):
        return str(self.value)


class Bool:
    def __init__(self, value):
        self.type = 'bool'
        self.value = value

    def simplify(self, program_state):
        return self

    def __str__(self):
        values = ['False', 'True']
        return values[self.value]


class Char:
    def __init__(self, value):
        self.type = 'char'
        self.value = value

    def simplify(self, program_state):
        return self

    def __str__(self):
        return "'" + self.value + "'"


class String:
    def __init__(self, value):
        self.type = 'string'
        self.value = value

    def simplify(self, program_state):
        return self

    def __str__(self):
        return '"' + str(self.value) + '"'


class Alias:
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

    def __str__(self):
        return str(self.var) + '@' + str(self.expr)

    def simplify(self, program_state):
        return self


class Collection:
    def __init__(self, items=[], operator=None):
        self.items = items
        self.operator = operator

    def simplify(self, program_state):
        if self.operator.name == ',':
            return Tuple(list(filter(lambda item: item != None, self.items)),
                         program_state)

        if len(self.items) == 2:
            left = self.items[0]
            if left: left = left.simplify(program_state)
            right = self.items[1]
            if right: right = right.simplify(program_state)
            return self.operator.apply(left, right, program_state)
        for i in range(len(self.items) - 1):
            if (not self.operator.apply(self.items[i].simplify(program_state),
                                        self.items[i + 1].simplify(program_state), program_state).value):
                return Bool(False)
        return Bool(True)

    def __str__(self):
        string = list(map(str, self.items))
        return '(' + (' ' + self.operator.name + ' ').join(string) + ')'


class Module:
    def __init__(self, name, code, program_state):
        self.name = name
        self.state = {}
        program_state.frame_stack.append(self.state)
        program_state.evaluate(code)
        program_state.frame_stack.pop(-1)
        program_state.frame_stack[-1].update(self.state)

    def simplify(self, program_state):
        return self

    def __str__(self):
        return self.name


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
