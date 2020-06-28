# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 15:43:13 2019

@author: rohan
"""
from Modules.List import *
from Modules.Maybe import *
from Modules.Char import *

functionNames = ['id', 'const', 'mod', 'rem', 'quot', 'fst', 'snd', 'div', 'succ',
                 'pred', 'null', 'even', 'odd']
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

def fst(tup):
    return tup[0]

def snd(tup):
    return tup[1]

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
