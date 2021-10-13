# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:38:23 2020

@author: rohan
"""
from function import Func
from beaver_class import Class


class Expression:
    pass


class BinaryExpression(Expression):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left_expr = left
        self.right_expr = right

    def __str__(self):
        buf = '('
        if not self.left_expr:
            buf += '?'
        else:
            try:
                buf += str(self.left_expr)
            except:
                print(self.left_expr)
        string = self.operator.name
        buf += ' ' + string
        if string != ' ':
            buf += ' '
        if not self.right_expr:
            buf += '?'
        else:
            buf += str(self.right_expr)
        buf += ')'
        return buf

    def simplify(self, program_state):
        operator = self.operator
        if self.left_expr:
            left_expr = self.left_expr
            if not self.operator.lazy:
                left_expr = left_expr.simplify(program_state)
            operator = operator.apply(left_expr, program_state=program_state)
            if self.right_expr:
                right_expr = self.right_expr

                if not (self.operator.lazy or
                        self.operator.name == ' ' and
                        (issubclass(type(left_expr), Func) or type(left_expr) == Class)
                        and left_expr.lazy):
                    right_expr = self.right_expr.simplify(program_state)
                operator = operator.apply(right_expr,
                                          program_state=program_state)
                return operator

        if self.right_expr:
            right_expr = self.right_expr
            if not self.operator.lazy:
                right_expr = right_expr.simplify(program_state)
            operator = operator.apply(None, right_expr, program_state)

        return operator
