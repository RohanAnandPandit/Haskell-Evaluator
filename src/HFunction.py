# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 08:58:06 2020

@author: rohan
"""
from functools import partial

class HFunction:
    def __init__(self, precedence, associativity, func, noOfArgs, name = 'None'):
        self.name = name
        self.precedence = precedence
        self.associativity = associativity
        self.func = func
        self.noOfArgs = noOfArgs
        
    def apply(self, arg1 = None, arg2 = None):
        func = self.func
        noOfArgs = self.noOfArgs
        name = self.name
        if (arg1 != None):
            if (self.noOfArgs == 1):
                return self.func(arg1)
            
            func = partial(self.func, arg1)
            noOfArgs -= 1
            name += ' ' + str(arg1)

        if (arg2 != None):
            if (self.noOfArgs == 1):
                return self.func(arg2)

            func = partial(self.func, b = arg2)
            noOfArgs -= 1
            name += ' ' + str(arg2)
            
        return HFunction(self.precedence, self.associativity, func, noOfArgs, name) 
    
    def simplify(self):
        return self
    
    def toString(self):
        return self.name
    

class Composition:
    def __init__(self, second, first):
        self.first = first.simplify()
        self.second = second.simplify()
        self.precedence = self.first.precedence
        self.associativity = self.first.associativity
        self.noOfArgs = 1
    
    def apply(self, arg):
        if (arg != None):
            return self.second.apply(self.first.apply(arg))
        return self
    
    def simplify(self):
        return self
    
    def toString(self):
        return self.second.toString() + '.' + self.first.toString()