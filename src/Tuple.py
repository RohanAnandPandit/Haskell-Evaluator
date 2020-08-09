# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 10:19:03 2020

@author: rohan
"""
functionNamesTuple = ['fst', 'snd', 'swap']
class Tuple:
    def __init__(self, tup):
        self.tup = tup
       
    def simplify(self, simplifyVariables = True):
        from Expression import BinaryExpr
        from utils import typeNames
        tup = []
        for i in range(len(self.tup)):
            value = self.tup[i]
            if (simplifyVariables):
                value = self.tup[i].simplify()
            if isinstance(self.tup[i], BinaryExpr):
                if (self.tup[i].operator.name == ' ' 
                    and self.tup[i].leftExpr.name in typeNames):
                    value = BinaryExpr(value.operator, value.leftExpr,
                                       value.rightExpr.simplify(False))
                else:
                    value = value.simplify()
            tup.append(value)
                
        return Tuple(tup)
    
    def __str__(self):
        return '{' + ', '.join(list(map(str, self.tup))) + '}'

def fst(tup):
    return tup.tup[0]

def snd(tup):
    return tup.tup[1]

def swap(a):
    tup = a
    tup.tup = (tup.tup[1], tup.tup[0])
    return tup