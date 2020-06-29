# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:19:04 2020

@author: rohan
"""
from utils import dimensionOf
from HFunction import HFunction, Composition
from List import Nil, Cons, head
from Expression import Data, BinaryExpr
from Stack import Stack

def space(a, b):
    (func, arg) = (a, b)
    return func.apply(arg)

def dot(a, b):
    (second, first) = (a, b)
    return Composition(second, first)

def index(a, b):
    (arr, index) = (a, b)
    return arr[index]

def power(a, b):
    return a ** b

def divide(a, b):
    return a / b

def multiply(a, b):
    return a * b

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

   
def lessThan(a, b):
    return a < b

def lessThanOrEqual(a, b):
    return a <= b

def greaterThan(a, b):
    return a > b

def greaterThanOrEqual(a, b):
    return a >= b

def equals(a, b):
    return a == b

def notEqual(a, b):
    return a != b

def AND(a, b):
    return (a and b)

def OR(a, b):
    return (a or b)
'''
def cons(a, b):
    (x, xs) = (a, b)
    return [x] + xs
'''
def cons(a, b):
    (x, xs) = (a, b)
    return Cons(x, xs)

def concatenate(a, b):
    return a + b

def comprehension(a, b):
    from Operators import Operator
    from Shunting_Yard_Algorithm import addBinaryExpr

    operands = Stack()
    operators = Stack()
    if (isinstance(b, Cons)):
        b = head(b)
    if (type(a) == int):
        if (a <= b):
            start = a
            end = b + 1
            step = 1
        else:
            start = a
            end = b - 1
            step = -1

        for i in range(start, end, step):
            operands.push(i)
            operators.push(Operator.COLON.value)
        operands.push(Data(Nil()))
        while (operators.peek() != None):
            addBinaryExpr(operators, operands)
        expr = operands.pop()
    elif (type(a) == bool):
        pass
    return expr.simplify()
