# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 08:58:06 2020

@author: rohan
"""


class Func:
    pass


class HFunction(Func):
    def __init__(self, precedence, associativity, func,
                 no_of_args, name, inputs=[], lazy=False):
        self.name = name
        self.precedence = precedence
        self.associativity = associativity
        self.func = func
        self.no_of_args = no_of_args
        self.inputs = inputs
        self.lazy = lazy

    def execute(self, inputs):
        if self.no_of_args == len(inputs):
            for arg in inputs:
                if not arg:
                    return False
            return True
        return False

    def apply(self, arg1=None, arg2=None, program_state=None):
        inputs = self.inputs.copy()
        if arg1:
            if len(inputs) > 1 and not inputs[-2]:
                inputs[-2] = arg1
            else:
                inputs.append(arg1)

            if arg2:
                inputs.append(arg2)

        elif arg2:
            inputs.append(None)
            inputs.append(arg2)

        if self.execute(inputs):
            return self.call(inputs, program_state)

        return HFunction(self.precedence, self.associativity, self.func,
                         self.no_of_args, self.name, inputs=inputs,
                         lazy=self.lazy)

    def simplify(self, program_state):
        if self.execute(self.inputs):
            return self.func(program_state)
        return self

    def call(self, inputs, program_state):
        if self.no_of_args == 1:
            return self.func(inputs[0], program_state)
        if self.no_of_args == 2:
            return self.func(inputs[0], inputs[1], program_state)
        if self.no_of_args == 3:
            return self.func(inputs[0], inputs[1], inputs[2], program_state)
        if self.no_of_args == 4:
            return self.func(inputs[0], inputs[1], inputs[2],
                             inputs[3], program_state)

    def __str__(self):
        return self.name

    def clone(self):
        return HFunction(self.precedence,
                         self.associativity, self.func, self.no_of_args,
                         self.name)


class Composition(Func):
    def __init__(self, second, first):
        self.first = first
        self.second = second
        # self.precedence = first.precedence
        # self.associativity = first.associativity
        self.name = str(second) + '~' + str(first)
        self.lazy = self.first.lazy

    def simplify(self, program_state):
        return self

    def __str__(self):
        return self.name

    def apply(self, arg1=None, program_state=None):
        if arg1 is not None or self.first.name == '..':
            return self.second.apply(
                self.first.apply(arg1, program_state=program_state),
                program_state=program_state)

        return self


class Function(Func):
    def __init__(self, name, cases=[], inputs=[]):
        self.name = name
        self.cases = cases
        self.inputs = inputs
        from operators import Associativity
        self.associativity = Associativity.LEFT
        self.precedence = 8
        self.lazy = False

    def clone(self):
        return Function(self.name,
                        list(map(lambda case:case.clone(), self.cases)),
                        self.inputs.copy())

    def simplify(self, program_state):
        value = self.check_cases(self.inputs, program_state)
        if value is not None:
            return value
        return self

    def __str__(self):
        return self.name

    def apply(self, arg1=None, arg2=None, program_state=None):
        inputs = self.inputs.copy()
        if arg1:
            if len(inputs) > 1 and not inputs[-2]:
                inputs[-2] = arg1
            else:
                inputs.append(arg1)
            if arg2:
                inputs.append(arg2)

        elif arg2:
            inputs.append(None)
            inputs.append(arg2)

        value = self.check_cases(inputs, program_state)
        if value is not None:
            return value
        return Function(self.name, cases=self.cases, inputs=inputs)

    def check_cases(self, inputs, program_state):
        for case in self.cases:
            arguments = case.arguments
            if len(arguments) == len(inputs):
                if self.match_case(arguments, inputs, program_state):
                    for i in range(len(arguments)):
                        case = case.apply(inputs[i].simplify(program_state),
                                          program_state=program_state)
                    if not case:
                        continue

                    return case.simplify(program_state)
        # raise Exception('''Pattern match on arguments failed for all
        # definitions of function''', self.name)
        return None

    def match_case(self, arguments, inputs, program_state):
        from utils import pattern_match

        if len(inputs) != len(arguments):
            return False

        for i in range(len(arguments)):
            if not pattern_match(arguments[i], inputs[i], program_state):
                return False

        return True


class Lambda(Func):
    def __init__(self, name, expr, arguments=[], inputs=[],
                 return_type=None, initial_state=None):
        self.name = name
        self.arguments = arguments
        self.expr = expr
        self.inputs = inputs
        self.no_of_args = len(arguments)
        self.lazy = False
        self.return_type = return_type
        self.state = initial_state
        if initial_state is None:
            self.state = {}

    def clone(self):
        state = self.state.copy()
        return Lambda(self.name, self.expr, self.arguments, self.inputs,
                      self.return_type, state)

    def apply(self, arg1=None, arg2=None, program_state=None):
        inputs = self.inputs.copy()

        if arg1:
            if len(inputs) > 1 and not inputs[-2]:
                inputs[-2] = arg1
            else:
                inputs.append(arg1)

            if len(inputs) == self.no_of_args:
                return self.return_value(inputs, program_state)

            if arg2:
                inputs.append(arg2)
                if len(inputs) == self.no_of_args:
                    return self.return_value(inputs, program_state)

        elif arg2:
            inputs.append(None)
            inputs.append(arg2)

        return Lambda(self.name, self.expr, self.arguments, inputs)

    def __str__(self):
        string = '\\' + ' '.join(list(map(str, self.arguments)))
        if self.expr:
            string += ' -> ' + str(self.expr)

        return string

    def simplify(self, program_state):
        if self.no_of_args == 0:
            return self.return_value([], program_state).simplify(program_state)
        return self

    def return_value(self, inputs, program_state):
        from operator_functions import assign
        state = self.state

        for i in range(self.no_of_args):
            assign(self.arguments[i], inputs[i], program_state, state)

        program_state.frame_stack.append(state)
        value = self.expr.simplify(program_state)
        program_state.frame_stack.pop(-1)
        program_state.return_value = None

        return value
