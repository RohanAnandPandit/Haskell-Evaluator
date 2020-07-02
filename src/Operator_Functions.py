# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:19:04 2020

@author: rohan
"""
from utils import dimensionOf, state, functionNames, isPrimitive
from HFunction import HFunction, Composition
from List import List, Nil, Cons, head
from Expression import Data, BinaryExpr
from Stack import Stack

def assign(a, b):
    from Operators import operatorsDict, Op

    state[a] = b
    if (type(b) in [HFunction, Composition]):
        functionNames.append(a)
        operatorsDict[a] = Op(b)
        b.name = a
    return b
    
def space(a, b):
    (func, arg) = (a, b)
    return func.apply(arg)

def dot(a, b):
    (second, first) = (a, b)
    return Composition(second, first)

def index(a, b):
    (xs, index) = (a, b)
    xs = xs.simplify()
    initialList = xs
    while (index >= 0 and isinstance(xs, Cons)):
        if (index == 0):
            value = xs.item
            if (not isPrimitive(xs.item)):
                value = xs.item.simplify()
            return value
        xs = xs.list
        index -= 1
    return None

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

def comma(a, b):
    if (type(a) == tuple):
        a = list(a)
        a.append(b)
        return tuple(a)
    return (a, b)
        
    
def cons(a, b):
    (x, xs) = (a, b)
    return Cons(x, xs)

def concatenate(a, b):
    (left, right) = (a, b)
    listType = left.type
    left = left.simplify()
    initialList = left
    if (isinstance(left, Nil)):
        return right
    while (not isinstance(left.list, Nil)):
        left = left.list
    left.list = right.simplify()  
    res = List(initialList)
    res.type = listType
    return res

def comprehension(a, b):
    from Operators import Operator
    from Shunting_Yard_Algorithm import addBinaryExpr

    numbers = []

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
            numbers.append(i)
    elif (type(a) == bool):
        pass
    return tuple(numbers)

def sequence(a, b): 
    (first, second) = (a, b)
    return
    
def chain(a, b):
    (first, second) = (a, b)
    from IO import WORLD
    
    if (isinstance(first, HFunction)):
        try:
            first.apply()
        except:
            pass
    second.apply(WORLD[0])
    