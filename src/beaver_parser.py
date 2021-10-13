# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 09:35:26 2020

@author: rohan
"""
from stack import Stack
from function import HFunction, Lambda, Function
from operators import Associativity, operator_from_string
from expression import BinaryExpression
from beaver_list import Nil, Array
from beaver_tuple import Tuple
from beaver_types import Int
from collection import Collection


class Parser:
    def __init__(self, lexer, program_state, infix=False):
        self.lexer = lexer
        self.infix = infix
        self.operands = Stack()
        self.operators = Stack()
        self.program_state = program_state
        self.expr = self.parse()

    def create_expression(self):
        operator = self.operators.pop()
        right, left = self.operands.pop(), self.operands.pop()
        expr = BinaryExpression(operator, left, right)
        self.operands.push(expr)

    def create_collection(self):
        operator = self.operators.pop()
        right, left = self.operands.pop(), self.operands.pop()
        if isinstance(left, Collection) and left.operator.name == operator.name:
            left.items.append(right)
            expr = left
        else:
            if right is None and operator.name == ',':
                expr = Collection([left], operator)
            elif left is None and operator.name == ',':
                expr = Collection([right], operator)
            else:
                expr = Collection([left, right], operator)

        self.push_operand(expr)

    def add_operator(self, current):
        top_operator = self.operators.peek()
        # Checks if a BinaryExpr should be created using the operator on the 
        # top of the stack
        while top_operator is not None:
            if (top_operator.precedence == current.precedence
                    and current.associativity == top_operator.associativity ==
                    Associativity.NONE):
                self.create_collection()

            elif (top_operator.precedence > current.precedence
                  or top_operator.precedence == current.precedence
                  and top_operator.associativity == Associativity.LEFT):
                self.create_expression()

            else:
                break
            top_operator = self.operators.peek()
        self.operators.push(current)

    def push_operand(self, operand):
        # If the top of the self.operands is None it will be replaced with
        # the current value
        if not self.operands.peek():
            self.operands.pop()

        if (self.operators.peek() and self.operators.peek().name == '-' and
                not self.operands.peek()):
            self.operators.pop()
            operand = BinaryExpression(operator_from_string('*'), Int(-1), operand)

        self.operands.push(operand)

        # If there are no self.operators means the current value is the left
        # operand and the right one is undecided yet so None is added
        if not self.operators.peek():
            self.operands.push(None)
            # print(self.operands.arr)

    def parse(self):
        from utils import convertToList
        # Empty stacks will be created whenever the function is called again
        self.operands = Stack()
        self.operators = Stack()
        token = self.lexer.next_token()
        while token:
            if isinstance(token, (HFunction, Lambda, Function)):
                # If a bracket has been opened the expression within them is 
                # generated by 
                # recursively calling the function with the same self.lexer 
                # object 
                if token.name == '(':
                    if (isinstance(self.lexer.peek(), HFunction)
                            and self.lexer.peek().name == ')'):
                        self.lexer.next_token()
                        self.push_operand(Tuple([], self.program_state))
                    else:
                        expr = Parser(self.lexer, self.program_state).expr
                        self.push_operand(expr)

                elif token.name == ')':
                    self.add_remaining()
                    result = self.operands.pop()
                    if (isinstance(result, Collection) and
                            result.operator.name == ','):
                        result = Tuple(result.items, self.program_state)
                    return result

                elif token.name == '[':
                    if (isinstance(self.lexer.peek(), HFunction)
                            and self.lexer.peek().name == ']'):
                        self.lexer.next_token()
                        self.push_operand(Nil())
                    else:
                        expr = Parser(self.lexer, self.program_state).expr
                        self.push_operand(expr)

                elif token.name == ']':
                    self.add_remaining()
                    result = self.operands.pop()
                    if (isinstance(result, Collection) and
                            result.operator.name == ','):
                        result = convertToList(result.items, self.program_state)
                    else:
                        result = convertToList([result], self.program_state)
                    return result

                elif token.name == '{':
                    if (isinstance(self.lexer.peek(), HFunction)
                            and self.lexer.peek().name == '}'):
                        self.lexer.next_token()
                        self.push_operand(Array())
                    else:
                        expr = Parser(self.lexer, self.program_state).expr
                        self.push_operand(expr)

                elif token.name == '}':
                    self.add_remaining()
                    result = self.operands.pop()
                    if (isinstance(result, Collection) and
                            result.operator.name == ','):
                        result = Array(result.items)
                    else:
                        result = Array([result])

                    return result

                elif token.name == '`':
                    if self.infix:
                        break
                    else:
                        func = Parser(self.lexer, self.program_state,
                                      infix=True)
                        self.operands.pop() == None
                        expr = BinaryExpression(operator_from_string(' '), func,
                                                self.operands.pop())
                        self.push_operand(expr)
                        self.operators.push(operator_from_string(' '))
                else:
                    # Compares the current operator with the self.operators on the
                    # stack
                    self.add_operator(token)
            else:
                self.push_operand(token)
            # Gets next token
            token = self.lexer.next_token()

        self.add_remaining()
        return self.operands.pop()

    def add_remaining(self):
        # Dealing with any remaining self.operators
        while self.operators.peek() is not None:
            if self.operators.peek().associativity == Associativity.NONE:
                self.create_collection()
            else:
                self.create_expression()

        if self.operands.peek() is None:
            self.operands.pop()

    def print_state(self):
        print("=================")
        print("self.operands")
        for operand in self.operands.arr:
            if operand is None:
                print('Parser print_state:', 'None')
                continue
            print(operand)
        print("=================")
        print("self.operators")
        for op in self.self.operators.arr:
            if op is None:
                print('Parser print_state:', 'None')
                continue
            print("'" + str(op) + "'")
        print("=================")
        print()