# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 15:43:13 2019

@author: rohan
"""
from List import *
from Maybe import *
from Char import *
from Tuple import *
from IO import *
from HFunction import HFunction

functionNamesPrelude = ['id', 'const', 'mod', 'rem', 'quot', 'div', 'succ',
                        'pred', 'null', 'even', 'odd', 'flip', 'not']
def id(x):
    return x

def const(x, y):
    return x

def mod(a, b):
    return a % b

def rem(a, b):
    return a % b

def quot(a, b):
    return a // b


def div(a, b):
    return a // b

def succ(x):
    return x + 1

def pred(x):
    return x - 1

def null(l):
    return l == [] or l == ''

def even(n):
    return n & 1 == 0

def odd(n):
    return n & 1 == 1

def flip(a):
    hfunc = a.simplify()
    return HFunction(hfunc.precedence, hfunc.associativity, lambda x, y : hfunc.func(y, x),
                     hfunc.noOfArgs, 'flip ' + hfunc.toString())

def notHaskell(a):
    return not a
