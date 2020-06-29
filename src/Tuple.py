# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 10:19:03 2020

@author: rohan
"""

functionNamesTuple = ['fst', 'snd', 'swap']

class Tuple:
    def __init__(self, expr):
        self.expr = expr
       
    def simplify(self):
        self.expr = self.expr.simplify()
        return self
    
    def toString(self):
        from List import listString
        
        return listString(self.expr.simplify(), '(')

def fst(tup):
    from List import Cons

    tup.simplify()
    expr = tup.expr
    if (isinstance(expr, Cons)):
        return expr.item
    
    return None

def snd(tup):
    from List import Cons

    tup.simplify()
    expr = tup.expr
    if (isinstance(expr, Cons)):
        expr = expr.list
        if (isinstance(expr, Cons)):
            return expr.item
        
    return None

def swap(tup):
    tup.simplify()
    expr = tup.expr
    first = expr.item
    second = expr.list.item
    temp = first
    expr.item = second
    expr.list.item = temp
    
    return tup