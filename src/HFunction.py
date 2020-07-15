# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 08:58:06 2020

@author: rohan
"""
from functools import partial
class HFunction:
    def __init__(self, precedence, associativity, func, noOfArgs, name = 'None', args = []):
        self.name = name
        self.precedence = precedence
        self.associativity = associativity
        self.func = func
        self.noOfArgs = noOfArgs
        self.args = args
        self.currentArg = 1
        
    def apply(self, arg1 = None, arg2 = None):
        from Tuple import Tuple
        
        if (self.name == '..' and isinstance(arg2, Tuple)):
            (arg1, arg2) = (arg2, None)
        if (self.noOfArgs == 0):
            return self.func()
            
        func = self.func
        noOfArgs = self.noOfArgs
        name = self.name
        if (arg1 != None):
            name += ' ' + str(arg1)
            if (self.noOfArgs == 1):
                return func(arg1)
            
            func = partial(func, arg1)
            noOfArgs -= 1
            
        if (arg2 != None or self.name == '..'):
            name += ' ' + str(arg2)
            if (noOfArgs == 1):
                return func(arg2)

            func = partial(func, b = arg2)
            noOfArgs -= 1
            name += ' ' + str(arg2)
            
        return HFunction(self.precedence, self.associativity, func, noOfArgs, name) 
    
    def simplify(self, state, simplifyVariables):
        if (self.name[0] == '\\'):
            return self.func()
        return self
    
    def __str__(self):
        if (self.name == '\\'):
            try:
                return self.name + ' '.join(map(str, list(self.func.args)))
            except:
                pass
        return self.name
    
    def clone(self):
        return HFunction(self.precedence, self.associativity, self.func, self.noOfArgs, self.name)
    
class Composition:
    def __init__(self, second, first):        
        self.first = first.simplify({}, False)
        self.second = second.simplify({}, False)
        self.precedence = first.precedence
        self.associativity = first.associativity
        self.name = str(second) + '.' + str(first)
    
    def simplify(self, a, b):
        return self
    
    def __str__(self):
        return self.name
    
    def apply(self, arg1 = None):
        if (arg1 != None or self.first.name == '..'):
            return self.second.apply(self.first.apply(arg1))
        return self

class Lambda:
    def __init__(self, name = None, arguments = [], expr = None, state = {}):
        self.name = name
        self.arguments = arguments
        self.expr = expr
        self.state = state
        
    def apply(self, arg):
        from Operator_Functions import assign
        s = self.state.copy()
        assign(self.arguments[0], arg, s)
        if (len(self.arguments) == 1):
            return self.expr.simplify(s, True)
        return Lambda(arguments = self.arguments[1:], expr = self.expr, state = s)
    
    def __str__(self):
        return '\\' + ' '.join(list(map(str, self.arguments))) + ' -> ' + str(self.expr)
    
    def simplify(self, a, b):
        if (self.arguments == []):
            return self.expr.simplify(self.state, True)
        return self