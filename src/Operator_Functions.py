# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:19:04 2020

@author: rohan
"""
from utils import builtInState, functionNames, Variable
from HFunction import HFunction, Composition, Lambda
from List import Nil, Cons, Iterator, head, tail
from Tuple import Tuple, fst, snd

def assign(a, b, state = builtInState):
    (var, value) = (a, b) 
    if (isinstance(a, Cons)):
        v, vs = head(a), tail(a)
        if (type(v) != str):
            v = v.simplify(state, False)
        assign(v, head(b))
        if (vs != None):
            assign(vs, tail(b))
    elif (isinstance(a, Tuple)):
        varTup = a.tup
        valTup =  b.tup
        for i in range(len(varTup)):
            assign(varTup[i], valTup[i])          
    else:
        state[var.name] = value
        if (value in (HFunction, Composition, Lambda)):
            builtInState[var.name] = value
            functionNames.append(var.name)
    return value
    
def space(a, b):
    (func, arg) = (a, b)
    if (isinstance(func, Variable)):
        func = func.simplify({}, True)
    return func.apply(arg)

def dot(a, b):
    (second, first) = (a, b)
    return Composition(second, first)

def index(a, b):
    from List import head, tail
    n = b
    if (n < 0 or isinstance(a, Nil)):
        return None
    x, xs = head(a), tail(a) 
    if (n == 0):
        return x
    return index(xs, n - 1)

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
    if (isinstance(a, Tuple)):
        tup = a.tup
        tup.append(b)
        return Tuple(tup)
    return Tuple([a, b]) 
        
    
def cons(a, b):
    (x, xs) = (a, b)
    try:
        listType = xs.type
    except:
        listType = None
    return Cons(x, xs, listType)
    

def concatenate(a, b): 
    from List import head, tail
    
    (left, right) = (a, b)
    if (isinstance(left, Nil)):
        return right
    elif (isinstance(right, Nil)):
        return left
    x, xs = head(left), tail(left)
    return Cons(x, concatenate(xs, right))
 
def comprehension(a, b):    
    if (type(a) in [int, float] or isinstance(a, Tuple)):
        step = 1
        if (isinstance(a, Tuple)):
            a.tup = a.tup[1 : ]
            if (len(a.tup) == 1):
                start = fst(a)
            else:
                (first, second) = (fst(a), snd(a))
                start = first
                step = second - first
        else:            
            start = a
        end = b
        func_succ = state['succ']
        hfunc = func_succ.clone()
        hfunc.func = lambda x: x + step
        iterations = None
        if (end != None):
            iterations =  int(abs((end - start) / step))
        iterator = Iterator(func = hfunc, item = start, iterations = iterations, 
                        iteratorType = 'comprehension', step = step, end = end)
        return Cons(iterator, Nil())
 
    elif (type(a) == bool):
        pass

def sequence(a, b): 
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

def collect(*args):
    return args

def createLambda(args, expr, state = None):
    from HFunction import Lambda
    arguments = []
    args = args.simplify({}, False)
    name, variables = args[0].name, args[1:]
    for var in variables:
        arguments.append(var.simplify({}, False))
    func = Lambda(name, arguments = arguments, expr = expr)
    if (name != None):
        builtInState[name] = func
        functionNames.append(name)

    if (state != None):
        state[name] = func
        
    return func

def where(func, exp):
    exp.simplify(func.state, True)