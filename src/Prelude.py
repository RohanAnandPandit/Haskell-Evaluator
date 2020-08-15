# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 15:43:13 2019

@author: rohan
"""
from List import Nil
from Tuple import Tuple, fst, snd
import utils
from Types import Bool
from List import *
from Tuple import *
from Maybe import *
from Char import *
from IO import *

functionNamesPrelude = ['id', 'const', 'mod', 'rem', 'quot', 'div', 'succ',
                        'pred', 'null', 'even', 'odd', 'flip', 'not', 'uncurry',
                        'curry', 'for']
def idHaskell(x):
    return x

def const(x, y):
    return x

def mod(a, b):
    return utils.getData(a.value % b.value)

def rem(a, b):
    return utils.getData(a.value % b.value)

def quot(a, b):
    return utils.getData(a.value // b.value)

def div(a, b):
    return utils.getData(a.value // b.value)

def succ(x):
    return utils.getData(x.value + 1)

def pred(x):
    return utils.getData(x.value - 1)

def null(a):
    return Bool(a.value == None)

def empty(a):
    return Bool(isinstance(a, Nil))

def even(n):
    return Bool(n.value & 1 == 0)

def odd(n):
    return Bool(n & 1 == 1)

def flip(a):
    hfunc = a.clone()
    hfunc.name = 'flip ' + hfunc.name
    func = hfunc.func
    hfunc.func = lambda x, y : func(y, x)
    return hfunc

def notHaskell(a):
    return Bool(not a.value)

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

def forHaskell(assign, cond, after, stat, ret):
    from utils import frameStack
    state = {}
    frameStack.append(state)
    assign.simplify()
    while (cond.simplify().value):
        stat.simplify()
        after.simplify()
    value = ret.simplify()
    frameStack.pop(-1)
    return value
