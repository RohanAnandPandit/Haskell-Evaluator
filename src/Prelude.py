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
from Tuple import Tuple, fst, snd

functionNamesPrelude = ['id', 'const', 'mod', 'rem', 'quot', 'div', 'succ',
                        'pred', 'null', 'even', 'odd', 'flip', 'not', 'uncurry',
                        'curry']
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
    hfunc = a.clone()
    hfunc.name = 'flip ' + hfunc.name
    func = hfunc.func
    hfunc.func = lambda x, y : func(y, x)
    return hfunc

def notHaskell(a):
    return not a

def uncurry(a):
    hfunc = a.clone()
    hfunc.name = 'uncurry ' + hfunc.name
    func = hfunc.func
    hfunc.func = lambda tup: func(fst(tup), snd(tup))
    hfunc.noOfArgs = 1
    return hfunc

def curry(a):
    hfunc = a.clone()
    hfunc.name = 'curry ' + hfunc.name
    func = hfunc.func
    hfunc.func = lambda x, y: func(Tuple((x, y)))
    hfunc.noOfArgs = 2
    return hfunc