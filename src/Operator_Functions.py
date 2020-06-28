# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:19:04 2020

@author: rohan
"""
from utils import dimensionOf
from HFunction import Composition

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

def cons(a, b):
    (x, xs) = (a, b)
    return [x] + xs

def concatenate(a, b):
    return a + b

def comma(a, b):
    diff = dimensionOf(b) - dimensionOf(a)
    if (diff == 1):
        b = list(b)
        b = [a] + b
        return tuple(b)
    elif (diff == 0):
        return (a, b)

def comprehension(a, b):
    lis = []
    if (type(a) == int):
        if (a <= b):
            end = b + 1
            step = 1
        else:
            end = b - 1
            step = -1
        for i in range(a, end, step):
            lis.append(i)
    elif (type(a) == bool):
        pass
    return lis
