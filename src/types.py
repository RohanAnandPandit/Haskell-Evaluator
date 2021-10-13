# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 14:51:39 2020

@author: rohan
"""
from function import Func


class Variable:
    def __init__(self, name):
        self.name = name

    def simplify(self, program_state):
        if self.name == '_ ...':
            return self

        frame_stack = program_state.frame_stack
        for curr in frame_stack[::-1]:
            if self.name in curr.keys():
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
        from operator_functions import (default_int, default_float, default_bool,
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


