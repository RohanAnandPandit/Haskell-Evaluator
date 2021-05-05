# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:20:56 2020

@author: rohan
"""
from utils import is_primitive
from Types import Variable, Char, String
from Operators import operator_from_string
from HFunction import HFunction, Function, Lambda
from Types import Int, Float, Bool, Null


class Lexer:
    def __init__(self, string, program_state):
        self.tokens = []
        self.string = string
        self.index = 0
        self.curr = 0
        self.program_state = program_state
        self.tokenize()

    def next_token(self):
        value = self.peek()
        self.index += 1
        return value

    def peek(self):
        if self.index >= len(self.tokens):
            return None
        value = self.tokens[self.index]
        return value

    def printTokens(self):
        tokens = []
        for token in self.tokens:
            tokens.append(str(token))
        print(tokens)

    def add_space(self, op=' ', high_precedence=False):
        if len(self.tokens) > 0:
            lastToken = self.tokens[-1]
            if (op == '\n' and isinstance(lastToken, HFunction)
                    and lastToken.name == ' '):
                self.tokens.pop(-1)
                lastToken = self.tokens[-1]
            if (not isinstance(lastToken, (HFunction, Function, Lambda))
                    or not lastToken.name in self.program_state.operators
                    or lastToken.name in ')]}'):
                oper = operator_from_string(op)
                if high_precedence:
                    oper = oper.clone()
                    oper.precedence += 50
                self.tokens.append(oper)

    def add_string(self):
        start = self.curr
        escape = False
        while not (self.string[self.curr] == '"' and not escape):
            escape = False
            if self.string[self.curr] == '\\':
                escape = True

            self.curr += 1

        string = self.string[start: self.curr].replace('\\n', '\n')
        string = string.replace('\\"', '"')
        string = string.replace('\\t', '\t')
        self.tokens.append(String(string))
        self.curr += 1

    def add_operator(self, op):
        op = op.replace('\t', '')
        if op in ' \n':
            self.add_space(op)
            return

        if op not in '[({':
            if (len(self.tokens) > 0
                    and isinstance(self.tokens[-1], (HFunction, Function))
                    and self.tokens[-1].name in '; '):
                del self.tokens[-1]

        if op == '(':
            if len(self.tokens) > 0:
                if (isinstance(self.tokens[-1], Variable) or
                        self.tokens[-1].name == ')'):
                    # function call
                    high_precedence = False
                    self.add_space(high_precedence=high_precedence)

        if op in '[{':
            if len(self.tokens) > 0:
                if (isinstance(self.tokens[-1], (Variable, String)) or
                        self.tokens[-1].name in ']})'):
                    self.tokens.append(operator_from_string('!!'))

        self.tokens.append(operator_from_string(op))

    def add_data(self, data):
        data = data.replace('\t', '')
        if data in ('where', 'in', 'implements', 'extends', 'then', 'else'):
            return self.add_operator(data)

        # Implicit multiplication to variable
        if data != '':
            i = 0
            while (i < len(data) and
                   ('0' <= data[i] <= '9' or
                    data[i] in '._')):
                i += 1

            if i == 0 or i == len(data):
                self.tokens.append(self.get_data(data))
            else:
                self.tokens.append(self.get_data(data[:i]))
                self.tokens.append(operator_from_string('*'))
                self.tokens.append(self.get_data(data[i:]))

    def tokenize(self):
        while self.curr < len(self.string):
            if self.string[self.curr] == '\t':
                self.curr += 1
                continue

            # Skip over comment
            if self.string[self.curr] == '#':
                self.curr += 1
                while self.string[self.curr] not in '#\n':
                    self.curr += 1
                    if self.curr == len(self.string):
                        return
                self.curr += 1
                continue

            # Get string
            if self.string[self.curr] == '"':
                self.curr += 1
                self.add_string()
                continue

            # Get character
            elif self.string[self.curr] == "'":
                if self.curr + 1 < len(self.string):
                    char = self.string[self.curr + 1]
                    if (self.curr + 2 < len(self.string) and
                            self.string[self.curr + 2] == "'" and char != "'"):
                        self.tokens.append(Char(char))
                        self.curr += 3
                        continue

            elif self.string[self.curr] == '_':
                self.add_data('_')
                self.curr += 1
                continue

            if self.curr < len(self.string) - 1:
                if self.string[self.curr: self.curr + 2] == '..':
                    if (self.curr < len(self.string) - 2
                            and self.string[self.curr + 2] == '.'):
                        self.tokens.append(Variable('...'))
                        self.curr += 3
                    else:
                        self.add_operator('..')
                        self.curr += 2
                    continue

            # Find longest operator
            if self.string[self.curr] in self.program_state.operators:
                end = self.curr + 1
                while (end < len(self.string) and
                       self.string[end] in self.program_state.operators and
                       not (self.string[end] in '\n ()[]{}' or
                            self.string[end - 1] in '{}[]() \n')):
                    end += 1

                self.add_operator(self.string[self.curr: end])
                self.curr = end
                continue

            else:
                # Find longest variable or number
                end = self.curr + 1
                start_char = self.string[self.curr]

                while (end < len(self.string) and
                       (self.string[end] not in self.program_state.operators
                        or (self.string[end] in '._' and
                            '0' <= self.string[end - 1] <= '9' and
                            '0' <= start_char <= '9'))):
                    end += 1

                self.add_data(self.string[self.curr: end])
                self.curr = end
                continue

        self.add_data(self.string[self.curr:])
        self.add_space(' ')
        if len(self.tokens) > 0:
            del self.tokens[-1]

    # Determine type of data
    def get_data(self, exp):
        if is_primitive(exp):
            return exp

        if '.' in str(exp):
            if int(float(exp)) == float(exp):
                return Int(int(float(exp)))
            return Float(round(float(exp), 10))
        try:
            return Int(int(exp))
        except:
            pass

        if exp == 'True':
            return Bool(True)
        elif exp == 'False':
            return Bool(False)
        if exp == '?':
            return Null()

        from Types import Variable
        return Variable(exp)
